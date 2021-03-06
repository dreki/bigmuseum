"""Holds utilities for working with MongoDB aggregation pipelines."""
from __future__ import annotations

import datetime
from contextlib import asynccontextmanager
from functools import singledispatch
from typing import Any, Dict, List, Optional, Sequence, Type, TypeVar, Union

import dateparser
import humps
from db import AIOEngine
from models.model import Model
from motor.motor_asyncio import AsyncIOMotorCollection
from motor.motor_tornado import MotorCommandCursor
from odmantic.field import FieldProxy


def paginate(aggregation: Sequence[Dict], skip: int, limit: int) -> Sequence[Dict]:
    """
    Add pagination support to an aggregation.
    The output of the aggregation will provide `count` and `items`.
    """
    # Add total count.
    aggregation = list(aggregation) + [{'$group': {'_id': 'items',
                                                   'total': {'$sum': 1},
                                                   'items': {'$push': '$$ROOT'}}}]
    # Paginate.
    aggregation = list(aggregation) + [{'$project': {'total': True,
                                                     'items': {'$slice': ['$items', skip, limit]}}}]
    return aggregation


def lookup(from_: str,
           as_: str,
           local_field: str = None,
           foreign_field: str = None,
           pipeline: List[Dict] = None,
           let: Optional[Dict] = None) -> Dict:
    """Construct a `lookup` MongoDB aggregation stage. Convenience method."""
    # Allow pipelines _or_ a straightforward match.
    if pipeline:
        return {'$lookup': {'from': from_,
                            'let': (let or {}),
                            'pipeline': pipeline,
                            'as': as_}}
    return {'$lookup': {'from': from_,
                        'localField': local_field,
                        'foreignField': foreign_field,
                        'as': as_}}

# def deref(model: Model, id_: str) -> Dict:
#     """Return a DBRef for the given model and ID."""
#     return {'$ref': f'{+type(model)}', '$id': id_}


def deref(field: Union[FieldProxy, Model], record: Model) -> Dict:
    """Return a DBRef for the given field and record."""
    # We accept `Model` due to static type checking, but we need a `FieldProxy`.
    if isinstance(field, Model):
        raise TypeError(f'Expected a FieldProxy, got {type(field)}')
    return {f'{+field}': {'$ref': f'{+type(record)}', '$id': record.id}}


def match_deref(field: Union[FieldProxy, Model], record: Model) -> Dict:
    """Return a `match` MongoDB aggregation stage for a given field and record."""
    # We accept `Model` due to static type checking, but we need a `FieldProxy`.
    if isinstance(field, Model):
        raise TypeError(f'Expected a FieldProxy, got {type(field)}')
    return {'$match': {'$and': [{f'{+field}.$ref': f'{+type(record)}'},
                                {f'{+field}.$id': record.id}]}}


def date_(date: datetime.datetime) -> Dict:
    """Make a MongoDB date from a Python `datetime.datetime`."""
    return {'$dateFromString': {'dateString': date.isoformat()}}


class MongoExpression:
    """Allows conveniently specifying MongoDB aggregation stages in Python code."""

    def __init__(self,
                 stage_name: str,
                 convert_kwargs_to_camel: bool = False,
                 wrap_with: Optional[MongoExpression] = None) -> None:
        """Initialize."""
        self.stage_name = stage_name
        self.convert_kwargs_to_camel = convert_kwargs_to_camel
        self.wrap_with = wrap_with

    def __call__(self, *args, **kwargs) -> Dict:
        """Return a usable MongoDB expression."""
        output: Dict = {}
        if args:
            first_arg: Any = args[0]
            # Support dict subclasses, like `SortExpression`.
            if issubclass(type(first_arg), dict):
                first_arg = dict(first_arg.items())
            output = {self.stage_name: first_arg}
            output.update(kwargs or {})
        if not args and self.convert_kwargs_to_camel and kwargs:
            kwargs = humps.camelize(kwargs)
            output = {self.stage_name: kwargs}
        if not args and not self.convert_kwargs_to_camel and kwargs:
            output = {self.stage_name: kwargs}
        if self.wrap_with:
            output = self.wrap_with(output)
        return output


match = MongoExpression('$match')

unwind = MongoExpression('$unwind', convert_kwargs_to_camel=True)

add_fields = MongoExpression('$addFields')

expr = MongoExpression('$expr')

match_expr = MongoExpression('$expr', wrap_with=match)

match_expr_eq = MongoExpression('$eq', wrap_with=match_expr)

eq = MongoExpression('$eq')

ne = MongoExpression('$ne')

regex_match = MongoExpression('$regexMatch')

and_ = MongoExpression('$and')

or_ = MongoExpression('$or')

if_null = MongoExpression('$ifNull')

switch = MongoExpression('$switch')

case = MongoExpression('case')

count = MongoExpression('count')

add = MongoExpression('$add')

replace_root = MongoExpression('$replaceRoot', convert_kwargs_to_camel=True)

group = MongoExpression('$group')

push = MongoExpression('$push')

slice_ = MongoExpression('$slice')

size = MongoExpression('$size')

sort = MongoExpression('$sort')

limit = MongoExpression('$limit')

in_ = MongoExpression('$in')

not_ = MongoExpression('$not')

not_in = MongoExpression('$in', wrap_with=not_)

nin = MongoExpression('$nin')

exists = MongoExpression('$exists')

set_ = MongoExpression('$set')

unset = MongoExpression('$unset')

set_union = MongoExpression('$setUnion')

cond = MongoExpression('$cond')

subtract = MongoExpression('$subtract')

gt = MongoExpression('$gt')

literal = MongoExpression('$literal')

project = MongoExpression('$project')

replace_with = MongoExpression('$replaceWith')

TModel = TypeVar('TModel', bound=Model)


def aggregation_cursor(engine: AIOEngine,
                       aggregation: Sequence[Dict],
                       model: Type[TModel],
                       batch_size: int = None) -> MotorCommandCursor:
    """Run an aggregation pipeline and return a cursor that can be `async for`-ed."""
    collection: AsyncIOMotorCollection = engine.get_collection(model)
    if batch_size is not None:
        return collection.aggregate(aggregation,
                                    batchSize=batch_size)
    return collection.aggregate(aggregation)


async def aggregate_as_dicts(engine: AIOEngine,
                             aggregation: Sequence[Dict],
                             model: Type[TModel]) -> Sequence[Dict]:
    """
    Run an aggregation pipeline and return the results as dictionaries, without
    casting as a specific `Model`.

    :param engine: The engine to use.
    :param aggregation: The aggregation pipeline to run.
    :param model: The model whose collection to run the aggregation against.
    """
    cursor: MotorCommandCursor = aggregation_cursor(engine=engine,
                                                    model=model,
                                                    aggregation=aggregation)
    docs: Sequence[Dict] = await cursor.to_list(length=None)
    return docs


async def aggregate(engine: AIOEngine,
                    aggregation: Sequence[Dict],
                    model: Type[TModel]) -> Sequence[TModel]:
    """Run an aggregation pipeline and return the results as `Model` instances.

    :param engine: The engine to use.
    :param aggregation: The aggregation pipeline to run.
    :param model: The model whose collection to run the aggregation against.
    """
    # cursor: MotorCommandCursor = await aggregation_cursor(engine=engine,
    #                                                       model=model,
    #                                                       aggregation=aggregation)
    # docs: Sequence[Dict] = await cursor.to_list(length=None)
    # cast: Sequence[TModel] = [model.parse_doc(d) for d in docs]
    dicts: Sequence[Dict] = await aggregate_as_dicts(engine=engine,
                                                     aggregation=aggregation,
                                                     model=model)
    cast: Sequence[TModel] = [model.parse_doc(d) for d in dicts]
    return cast


async def aggregate_as(engine: AIOEngine,
                       aggregation: Sequence[Dict],
                       model: Type[TModel],
                       cast_to: Type[TModel]) -> Sequence[TModel]:
    """
    Run an aggregation pipeline, cast the documents to the appropriate `Model`,
    and return the results.

    :param engine: The engine to use.
    :param aggregation: The aggregation pipeline to run.
    :param model: The model whose collection to run the aggregation against.
    :param cast_to: The model to cast the documents to.
    """
    # cursor: MotorCommandCursor = aggregation_cursor(engine=engine,
    #                                                 model=model,
    #                                                 aggregation=aggregation)
    # docs: Sequence[Dict] = await cursor.to_list(length=None)
    docs: Sequence[Dict] = await aggregate_as_dicts(engine=engine,
                                                    aggregation=aggregation,
                                                    model=model)
    cast: Sequence[TModel] = [cast_to.parse_doc(d) for d in docs]
    return cast


@asynccontextmanager
async def start_transaction(engine: AIOEngine):
    """Execute MongoDB queries within a transaction."""
    async with await engine.client.start_session() as session:
        async with session.start_transaction():
            yield


async def aenumerate(asequence, start=0):
    """Asynchronously enumerate an async iterator from a given start value"""
    n = start
    async for elem in asequence:
        yield n, elem
        n += 1


async def yield_batches(cursor, batch_size):
    """
    Generator to yield batches from cursor
    """
    batch = []
    async for i, doc in aenumerate(cursor):
        if i % batch_size == 0 and i > 0:
            yield batch
            del batch[:]
        batch.append(doc)
    yield batch
