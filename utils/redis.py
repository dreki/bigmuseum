"""Holds Redis interface and utilities."""
from typing import Optional
import aioredis
from aioredis.client import Redis
from settings import ConfigurationException, settings

redis: Optional[Redis] = None


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
