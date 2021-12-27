"""Holds handlers for working with new Reddit posts."""
import asyncio
from asyncio.events import AbstractEventLoop
from concurrent.futures import Executor, ThreadPoolExecutor
from datetime import datetime
from typing import List, Optional, Sequence

# from praw.models.helpers import SubredditHelper
from asyncpraw import Reddit
from asyncpraw.models.helpers import SubredditHelper
from asyncpraw.reddit import Redditor, Submission, Subreddit
from db import get_engine
from models.post import Post
from models.session import Session
from models.user import User
from odmantic.engine import AIOEngine
from settings import settings
from tornado.web import HTTPError
from utils.log import logger
from utils.mongodb import aggregate, lookup, match, exists, project, replace_with, and_, eq, in_, unwind
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
        return posts

    async def get(self):
        """Handle GET request."""

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
