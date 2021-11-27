"""Holds utility for periodically downloading `Post`s."""
import asyncio
import datetime
from typing import Optional

from asyncpraw.reddit import Reddit, Submission
from db import AIOEngine, get_engine
from models.post import Post
from models.state import State

from utils.log import logger
from utils.reddit import get_reddit


async def _get_last_run(db: AIOEngine, create_if_missing=True) -> Optional[State]:
    """
    Get the last time the periodic download was run.

    Optionally create the record using the Unix epoch, if it doesn't exist.
    """
    last_run: Optional[State] = await db.find_one(State, {'key': 'last_post_cache'})
    if not last_run and create_if_missing:
        # Set to the epoch if there is no last run, so we get all posts.
        last_run = State(key='last_post_cache', value=datetime.datetime(1970, 1, 1))
    return last_run


async def _cache_posts():
    """Cache `Post`s from the subreddit."""
    # Get the most recent run of the download.
    db: AIOEngine = await get_engine()
    last_run = await _get_last_run(db, create_if_missing=True)
    if not last_run or type(last_run.value) is not datetime.datetime:
        # If the last run is not a datetime, then we can't use it.
        raise ValueError('Last run value is not a datetime, or is unexpectedly missing.')

    # Keep track of the last time we ran.
    new_last_run_stamp: datetime.datetime = datetime.datetime.now()

    reddit: Reddit = await get_reddit()
    r_museum = await reddit.subreddit('museum')
    logger.info('Caching posts from /r/museum')
    async for post in r_museum.hot(limit=5):
        # Convert created_utc to a datetime.
        post_created_utc: datetime.datetime = datetime.datetime.fromtimestamp(post.created_utc)
        if post_created_utc < last_run.value:
            continue
        post: Submission
        logger.info(f'> caching {post.title}')
        cached_post: Post = Post(post_id=post.id,
                                 title=post.title,
                                 image_url=post.url,
                                 post_created_at=datetime.datetime.fromtimestamp(post.created_utc))
        await db.save(cached_post)
        print(f'> cached:')
        print(cached_post)

    # Save the last time we ran.
    last_run.value = new_last_run_stamp
    await db.save(last_run)

    # Close the Reddit connection.
    await reddit.close()

    logger.info('Finished caching posts from /r/museum')


async def _do_periodically(interval_seconds, fn, *args, **kwargs):
    """Periodically calls `func` with `args` and `kwargs`."""
    while True:
        # Use `gather` to execute and ensure that the next execution isn't delayed.
        await asyncio.gather(*[
            asyncio.sleep(interval_seconds),
            fn(*args, **kwargs)
        ])


async def start():
    """Start the periodic download."""
    await _do_periodically(interval_seconds=60 * 5, fn=_cache_posts)
