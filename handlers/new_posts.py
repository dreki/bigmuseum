"""Holds handlers for working with new Reddit posts."""
# from typing import Dict, List, Optional, Sequence
from collections.abc import Sequence
from typing import Dict, List, Optional

# from praw.models.helpers import SubredditHelper
from asyncpraw import Reddit
from asyncpraw.reddit import Redditor, Submission, Subreddit
from db import get_engine
from models.post import Post
from models.user import User
from odmantic.engine import AIOEngine
from settings import settings
from tornado.web import HTTPError
from utils.json import dumps, loads
from utils.log import logger
from utils.mongodb import (aggregate, and_, eq, exists, in_, lookup, match,
                           project, replace_with, unwind)
from utils.redis import get_cache, set_cache, transaction
from utils.view_models.post import Post as PostViewModel

from handlers.base import BaseHandler


class NewPostsHandler(BaseHandler):
    """Returns new Reddit posts, given a person's account."""

    async def _get_cached_posts(self) -> Optional[Sequence[Dict]]:
        """Get cached posts, if they exist."""
        cache_key: str = self._make_cached_posts_key()
        logger.debug(f'> getting cached posts for {cache_key}')
        cached_posts: Optional[Sequence[Dict]] = await get_cache(Sequence[Dict], cache_key)
        return cached_posts

    async def _set_cached_posts(self, posts: Sequence[Post]) -> None:
        """Set cached posts."""
        cache_key: str = self._make_cached_posts_key()
        if not settings.get('new_posts_cache_expiration_seconds'):
            raise ValueError('NEW_POSTS_CACHE_EXPIRATION_SECONDS must be set in environment.')
        await set_cache(cache_key,
                        [p.dict() for p in posts],
                        expire_seconds=settings.get('new_posts_cache_expiration_seconds'))

    async def _fetch_posts(self) -> Sequence[Post]:
        """Fetch `Post`s from the database."""
        db: AIOEngine = await get_engine()
        # If a cache exists, use it.
        # logger.debug('> current user:')
        # logger.debug(self.current_user)
        # cache_key: str = f'{self.current_user.id}_new_posts'
        # # cached_posts: Optional[Sequence[Dict]] = await get_cache(cache_key)
        # cached_posts: Optional[Sequence[Dict]] = await get_cache(Sequence[Dict], cache_key)
        # if cached_posts:
        #     # logger.debug('> cached_posts:')
        #     # logger.debug(cached_posts)
        #     logger.debug('> returning cached posts')
        #     return [Post(**p) for p in cached_posts]

        # posts: List[Post] = await db.find(Post, Post.user == current_user.name)
        aggregation: List[dict] = [
            lookup(
                from_=+User,
                let={
                    f'{+User}_{+User.id}': self.current_user.id,  # type: ignore
                    f'{+Post}_{+Post.id}': ++Post.id,  # type: ignore
                },
                pipeline=[
                    replace_with(
                        should_hide=and_([
                            eq([++User.id, f'$${+User}_{+User.id}']),  # type: ignore  # noqa
                            in_([f'$${+Post}_{+Post.id}', ++User.hidden_posts]),  # type: ignore  # noqa
                        ])
                    )
                ],
                as_='hidden_filter'),
            unwind('$hidden_filter'),
            match({'hidden_filter.should_hide': False}),
            project(hidden=False)
        ]
        posts: Sequence[Post] = await aggregate(engine=db,
                                                aggregation=aggregation,
                                                model=Post)
        return posts

    async def get(self, filter: str):
        """Handle GET request."""

        # if not filter or filter not in ['new', 'hot', 'top']:
        if not filter or filter not in ['new']:
            raise HTTPError(status_code=400, reason='Invalid filter.')

        # TODO: Abstract this, and remove it from _get_posts
        cached_posts = await self._get_cached_posts()
        if cached_posts:
            await self.json({'items': cached_posts})
            return
        logger.debug('> cache missing; fetching posts')

        # Get information about the current Reddit user.
        # reddit: Optional[Reddit] = await self.make_reddit_client()
        # if not reddit:
        #     raise HTTPError(401, 'Reddit unauthorized')
        # # logger.debug('> dir(reddit.user):')
        # # logger.debug(dir(reddit.user.me()))
        # current_user: Optional[Redditor] = await reddit.user.me()
        # await reddit.close()
        # if not current_user:
        #     raise HTTPError(
        #         401, 'Expected current user to be found at reddit.user.me().')
        # logger.debug(current_user)

        # Load `Post`s from the database
        # db: AIOEngine = await get_engine()
        # logger.debug(f'> fetching posts for {current_user.name}')
        # posts: List[Post] = await db.find(Post)
        posts: Sequence[Post] = await self._fetch_posts()
        await self._set_cached_posts(posts)
        logger.debug('> returning posts')
        await self.json({'items': [p.dict() for p in posts]})
