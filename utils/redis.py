"""Holds Redis interface and utilities."""
from functools import singledispatch
from typing import Any, Dict, Optional, Sequence, Tuple, Type, TypeVar, Union, get_args, get_origin

import aioredis
from aioredis.client import Redis
from settings import ConfigurationException, settings

from utils.json import dumps, loads
from utils.log import logger

redis: Optional[Redis] = None


async def set_cache(key: str, value: Union[Sequence, Dict]):
    """Cache a value."""
    redis: Redis = await get_connection()
    await redis.set(key, dumps(value))


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


@singledispatch
async def get_cache__DEPRECATED(key: str) -> Optional[str]:
    """Get a value from the cache."""
    redis: Redis = await get_connection()
    value: Optional[str] = await redis.get(key)
    return value


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
    logger.debug(
        f'> type(value): {type(value)} expected_type: {expected_type}')
    # value = _ensure_type(expected_type, value)
    # return value
    return _ensure_type(expected_type, value)


def _ensure_type(expected_type: Type[T], value: Any) -> Optional[T]:
    """Ensure value is of expected type."""
    # If expected_type is a parameterized generic, check it and its parameter.
    type_args: Tuple = get_args(expected_type)
    type_origin: Optional[Any] = get_origin(expected_type)
    if not type_origin:  # For `str`, `int`, etc.
        type_origin = expected_type
    if not isinstance(value, type_origin):
        raise Exception(
            f'Expected type {expected_type} but got {type(value)}.')
    if type_args:
        # Note: Only checks first element.
        if isinstance(value, Sequence) and len(value) > 0:
            if not isinstance(value[0], type_args[0]):
                raise Exception(
                    f'Expected subscripted type {expected_type} but got {type(value)}.')
        # Note: Only checks first key-value pair.
        if isinstance(value, Dict) and len(value) > 0:
            first_key: Any = list(value.keys())[0]
            if not isinstance(first_key, type_args[0]):
                raise Exception(f'Expected subscripted key type {expected_type} '
                                f'but got {type(first_key)}.')
            first_value: Any = list(value.values())[0]
            if not isinstance(first_value, type_args[1]):
                raise Exception(f'Expected subscripted value type {expected_type} '
                                f'but got {type(first_value)}.')
    return value  # type: ignore
    # if not isinstance(value, expected_type):
    #     pass

# @get_cache.register
# async def _(expected_type: Type[T], key: int) -> Optional[T]:
#     pass

# @get_cache.register
# async def _(expected_type: Type[T], /, key: str) -> Optional[T]:
#     """Get a value from the cache."""
#     redis: Redis = await get_connection()
#     value: Optional[str] = await redis.get(key)
#     if value:
#         value = loads(value)
#         # if not expected_type:
#         #     return value
#         if not isinstance(value, expected_type):
#             raise Exception(f'Expected type {expected_type} but got {type(value)}.')
#         return value
#     return None


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
