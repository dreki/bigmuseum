"""Holds Redis interface and utilities."""
from contextlib import asynccontextmanager
from functools import singledispatch
from typing import Dict, Optional, Sequence, Type, TypeVar, Union

import aioredis
from aioredis.client import Pipeline, Redis
from settings import ConfigurationException, settings

from utils.json import dumps, loads
from utils.lang import ensure_type
from utils.log import logger

redis: Optional[Redis] = None


async def set_cache(key: str,
                    value: Union[Sequence, Dict],
                    expire_seconds: Optional[int] = None) -> None:
    """Cache a value."""
    # context: Union[Redis, Pipeline] = pipeline or await get_connection()

    redis: Redis = await get_connection()
    if expire_seconds:
        await redis.setex(name=key, value=dumps(value), time=expire_seconds)
        return
    await redis.set(key, dumps(value))
    # await redis.set(key, dumps(value))

    # await context.set(key, dumps(value))
    # if expire_seconds:
    #     await context.expire(key, expire_seconds)


async def delete_cache(key: str) -> None:
    """Delete a value from the cache."""
    redis: Redis = await get_connection()
    logger.debug(f'> Deleting cache for {key}')
    await redis.delete(key)


@asynccontextmanager
async def transaction():
    """
    Do a transaction. Async context manager.

    :yield: Redis transaction.
    """
    redis: Redis = await get_connection()
    # async with redis.multi() as multi:
    #     yield multi
    async with redis.pipeline(transaction=True) as pipeline:
        yield pipeline


T = TypeVar('T')
# async def get_cache(key: str, expected_type: Optional[T] = Dict) -> Optional[Union[Sequence, Dict]]:
# async def get_cache(key: str, expected_type: Optional[Type[T]] = Dict) -> Optional[T]:
#     """Get a value from the cache."""
#     redis: Redis = await get_connection()
#     value: Optional[str] = await redis.get(key)
#     if value:
#         value = loads(value)
#         if not expected_type:
#             return value
#         if expected_type and not isinstance(value, expected_type):
#             raise Exception(f'Expected type {expected_type} but got {type(value)}.')
#     return None


async def get_cache(expected_type: Type[T] = str, key: str = None) -> Optional[T]:
    """Get a value from the cache. Typed."""
    if not key:
        raise Exception('Key is required.')
    if not expected_type:
        raise Exception('Expected type is required.')
    redis: Redis = await get_connection()
    value: Optional[str] = await redis.get(key)
    if not value:
        return None
    value = loads(value)
    return ensure_type(expected_type, value)


async def get_connection() -> Redis:
    """Return a Redis connection."""
    global redis
    if redis:
        return redis
    if not settings.get('redis_host'):
        raise ConfigurationException(
            'redis_host is not defined in environment.')
    redis = aioredis.from_url(f'redis://{settings.get("redis_host")}')
    if not redis:
        raise Exception('Redis connection failed.')
    return redis
