"""Holds utility for periodically downloading `Post`s."""
import asyncio
import datetime

from asyncpraw.reddit import Reddit, Submission
from models.post import Post

from utils.reddit import get_reddit


async def _download_posts():
    """Downloads the `Post`s."""
    reddit: Reddit = await get_reddit()
    # for post in reddit.subreddit('museum').hot(limit=10):
    #     print(f'> Downloading {post.title} ({type(post)}')
    #     # post.download()
    # async for post in reddit.subreddit('museum').hot(limit=10):
    #     print(f'> Downloading {post.title} ({type(post)}')
    #     # post.download()

    r_museum = await reddit.subreddit('museum')
    async for post in r_museum.hot(limit=1):
        post: Submission
        print(f'> Downloading {post.title}')
        # print(dir(post))
        # breakpoint()
        # Timestamp to datetime
        cached_post: Post = Post(post_id=post.id,
                                 title=post.title,
                                 image_url=post.url,
                                 post_created_at=datetime.datetime.fromtimestamp(post.created_utc))
        print(f'> Downloaded:')
        print(cached_post)
    pass


async def _do_periodically(interval_seconds, func, *args, **kwargs):
    """Periodically calls `func` with `args` and `kwargs`."""
    while True:
        # Use `gather` to execute and ensure that the next execution isn't delayed.
        await asyncio.gather(*[
            asyncio.sleep(interval_seconds),
            func(*args, **kwargs)
        ])


def start():
    """Starts the periodic download."""
    asyncio.run(_do_periodically(60 * 5, _download_posts))
