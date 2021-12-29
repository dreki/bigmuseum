"""Holds handlers for working with new Reddit posts."""
# from typing import Dict, List, Optional, Sequence
from typing import Dict, List, Optional
from collections.abc import Sequence

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
from utils.redis import get_cache, set_cache
from utils.view_models.post import Post as PostViewModel

from handlers.base import BaseHandler

# class PostsHandler(BaseHandler):
#     """Handles requests for posts from Reddit."""

#     def __init__(self, loop: AbstractEventLoop, executor: Executor):
#         """Initialize the handler."""
#         super().__init__(loop, executor)

class NewPostsHandler(BaseHandler):
    """Returns new Reddit posts, given a person's account."""

    def _cool(self):
        logger.debug(f'> _cool')
        return 'neat'

    async def _fetch_posts(self, current_user: Redditor) -> Sequence[Post]:
        """Fetch `Post`s from the database."""
        db: AIOEngine = await get_engine()
        # If a cache exists, use it.
        logger.debug('> current user:')
        logger.debug(self.current_user)
        cache_key: str = f'{self.current_user.id}_new_posts'
        # cached_posts: Optional[Sequence[Dict]] = await get_cache(cache_key)
        cached_posts: Optional[Sequence[Dict]] = await get_cache(Sequence[Dict], cache_key)
        if cached_posts:
            # logger.debug('> cached_posts:')
            # logger.debug(cached_posts)
            logger.debug('> returning cached posts')
            return [Post(**p) for p in cached_posts]

        # posts: List[Post] = await db.find(Post, Post.user == current_user.name)
        aggregation: List[dict] = [
            lookup(from_=+User,
                   let={
                       f'{+User}_{+User.id}': self.current_user.id,  # type: ignore
                       f'{+Post}_{+Post.id}': ++Post.id,  # type: ignore
                   },
                   pipeline=[
                       replace_with(
                           should_hide=and_([
                               eq([++User.id, f'$${+User}_{+User.id}']),  # type: ignore
                               in_([f'$${+Post}_{+Post.id}', ++User.hidden_posts]),  # type: ignore
                            ])
                       )
                   ],
                   as_='hidden_filter'),
            unwind('$hidden_filter'),
            match({'hidden_filter.should_hide': False}),
            project(hidden=False)
        ]
        logger.debug('> aggregation:')
        logger.debug(aggregation)
        posts: Sequence[Post] = await aggregate(engine=db,
                                                aggregation=aggregation,
                                                model=Post)
        logger.debug('> settings:')
        logger.debug(settings)
        # logger.debug(ujson.dumps([p.dict() for p in posts]))
        logger.debug(dumps([p.dict() for p in posts]))
        logger.debug('Decoded:')
        decoded = loads(dumps([p.dict() for p in posts]))
        logger.debug(Post.parse_obj(decoded[0]))
        # redis: Redis = await get_connection()
        # await redis.set(f'{self.current_user.id}_new_posts', dumps(decoded))
        logger.debug(f'> cache_key: {cache_key}')
        await set_cache(cache_key, [p.dict() for p in posts])

        # posts[0].json
        # Post.parse_doc
        return posts

    async def get(self):
        """Handle GET request."""

        # TODO: Abstract this, and remove it from _get_posts
        cache_key: str = f'{self.current_user.id}_new_posts'
        cached_posts: Optional[Sequence[Dict]] = await get_cache(Sequence[Dict], cache_key)
        if cached_posts:
            await self.json({'items': cached_posts})
            return

        # Get information about the current Reddit user.
        reddit: Optional[Reddit] = await self.make_reddit_client()
        if not reddit:
            raise HTTPError(401, 'Reddit unauthorized')
        # logger.debug('> dir(reddit.user):')
        # logger.debug(dir(reddit.user.me()))
        current_user: Optional[Redditor] = await reddit.user.me()
        await reddit.close()
        if not current_user:
            raise HTTPError(
                401, 'Expected current user to be found at reddit.user.me().')
        logger.debug(current_user)

        # Load `Post`s from the database
        # db: AIOEngine = await get_engine()
        logger.debug(f'> fetching posts for {current_user.name}')
        # posts: List[Post] = await db.find(Post)
        posts: Sequence[Post] = await self._fetch_posts(current_user)
        logger.debug('> returning posts')
        await self.json({'items': [p.dict() for p in posts]})
