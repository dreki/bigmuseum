"""Holds handlers for working with new Reddit posts."""
import asyncio
from asyncio.events import AbstractEventLoop
from concurrent.futures import Executor, ThreadPoolExecutor
from datetime import datetime
from typing import List, Optional

# from praw.models.helpers import SubredditHelper
from asyncpraw import Reddit
from asyncpraw.models.helpers import SubredditHelper
from asyncpraw.reddit import Redditor, Submission, Subreddit
from db import get_engine
from models.post import Post
from models.session import Session
from odmantic.engine import AIOEngine
from settings import settings
from tornado.web import HTTPError
from utils.log import logger
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
            raise HTTPError(401, 'Expected current user to be found at reddit.user.me().')
        logger.debug(current_user)

        # Load `Post`s from the database
        db: AIOEngine = await get_engine()
        logger.debug(f'> fetching posts for {current_user.name}')
        posts: List[Post] = await db.find(Post)
        logger.debug('> returning posts')
        await self.json({'items': [p.dict() for p in posts]})

    async def get__DEPRECATED(self):
        """Handle GET request."""

        #
        # TODO: Get Posts from database instead of Reddit
        #

        logger.warn('> get__DEPRECATED')

        session: Session = await self.get_session()

        # aio_loop: AbstractEventLoop = asyncio.get_event_loop()
        # logger.debug(f'> loop {aio_loop}')
        # executor: Executor = ThreadPoolExecutor(max_workers=4)
        # # aio_loop.run_until_complete(self._cool())
        # result = await aio_loop.run_in_executor(executor=executor,
        #                                         func=self._cool)
        # logger.debug(f'> result {result}')

        # If no reddit credentials, return no auth
        if not session.reddit_credentials:
            self.set_status(401)
            return

        # reddit: AsyncReddit = AsyncReddit(
        reddit = Reddit(
            client_id=settings.get('reddit_client_id'),
            client_secret=settings.get('reddit_secret'),
            refresh_token=session.reddit_credentials.refresh_token,
            user_agent='bigmuseum by u/parsifal'
        )
        # r_museum: SubredditHelper = await reddit.subreddit('museum')
        # r_museum: SubredditHelper = await reddit.subreddit('museum',
        r_museum: Subreddit = await reddit.subreddit('museum')
        #  fetch=True)
        # logger.debug(f'> museum {dict(r_museum)}')
        logger.debug(dir(r_museum))
        # async for post in r_museum.new():
        first: bool = True
        posts: List[PostViewModel] = []
        async for submission in r_museum.hot(limit=15):
            submission: Submission
            logger.debug(
                f'> {submission.title} {submission.id} {submission.url} {submission.created} {submission.created_utc}')
            # logger.debug(dir(post))

            post = PostViewModel(id=submission.id,
                                 title=submission.title,
                                 link=submission.url,
                                 created_at=datetime.fromtimestamp(submission.created_utc))

            posts.append(post.to_dict())
            # if first:
            #     logger.debug(dir(post))
            #     logger.debug(post.media)
            #     logger.debug(post.media_embed)
            #     logger.debug(post.media_only)
            #     logger.debug(post.url)
            first = False

        # self.finish('hello')

        # self.finish({'items': posts})
        # self.finish(dumps({'items': posts}))
        await self.json({'items': posts})
