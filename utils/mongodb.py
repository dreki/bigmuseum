"""Holds utilities for working with MongoDB aggregation pipelines."""

from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional, Sequence, Type, Union

import humps
from pymongo.command_cursor import CommandCursor

from db import AIOEngine
from models.model import Model


def paginate(aggregation: Sequence[Dict], skip: int, limit: int) -> Sequence[Dict]:
    """
    Add pagination support to an aggregation.
    The output of the aggregation will provide `count` and `items`.
    """
    # Add total count.
    aggregation = aggregation + [{'$group': {'_id': 'items',
                                             'total': {'$sum': 1},
                                             'items': {'$push': '$$ROOT'}}}]
    # Paginate.
    aggregation = aggregation + [{'$project': {'total': True,
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


class MongoExpression:
    """Allows conveniently specifying MongoDB aggregation stages in Python code."""

    def __init__(self, stage_name: str, convert_kwargs_to_camel: bool = False):
        """Initializer"""
        self.stage_name = stage_name
        self.convert_kwargs_to_camel = convert_kwargs_to_camel

    def __call__(self, *args: Sequence, **kwargs: Dict) -> Dict:
        """Return a usable MongoDB expression."""
        if args:
            first_arg: Any = args[0]
            if issubclass(type(first_arg), dict):  # Support dict subclasses, like `SortExpression`.
                first_arg = dict(first_arg.items())
            output = {self.stage_name: first_arg}
            output.update(kwargs or {})
            return output
        if self.convert_kwargs_to_camel:
            kwargs = humps.camelize(kwargs)
        return {self.stage_name: kwargs}


match = MongoExpression('$match')

unwind = MongoExpression('$unwind', convert_kwargs_to_camel=True)

add_fields = MongoExpression('$addFields')

expr = MongoExpression('$expr')

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

nin = MongoExpression('$nin')

set_ = MongoExpression('$set')

set_union = MongoExpression('$setUnion')

cond = MongoExpression('$cond')

subtract = MongoExpression('$subtract')

gt = MongoExpression('$gt')

literal = MongoExpression('$literal')

project = MongoExpression('$project')


def aggregation_cursor(engine: AIOEngine,
                       aggregation=Sequence[Dict],
                       model: Type[Model] = None,
                       batch_size: int = None) -> CommandCursor:
    """Run an aggregation pipeline and return a cursor that can be `async for`-ed."""
    if batch_size is not None:
        return engine.get_collection(model).aggregate(
            aggregation, batchSize=batch_size)
    return engine.get_collection(model).aggregate(aggregation)


async def aggregate(engine: AIOEngine,
                    aggregation: Sequence[Dict],
                    model: Type[Model] = None,
                    cast_to: Type[Model] = None) -> Union[Sequence[Dict], Sequence[Model]]:
    """Run an aggregation pipeline, cast the documents to the appropriate `Model`, and return the results."""
    if not model and cast_to:
        model = cast_to
    if not model:
        raise ValueError('Must provide `model` or `cast_to`.')
    cursor: CommandCursor = aggregation_cursor(engine=engine, model=model, aggregation=aggregation)
    docs: Sequence[Dict] = await cursor.to_list(length=None)
    if not cast_to:
        return docs
    cast: Sequence[cast_to] = [cast_to.parse_doc(d) for d in docs]
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
