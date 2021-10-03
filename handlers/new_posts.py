"""Holds handlers for working with new Reddit posts."""
import asyncio
from asyncio.events import AbstractEventLoop
from concurrent.futures import Executor, ThreadPoolExecutor

# from praw.models.helpers import SubredditHelper
from asyncpraw import Reddit
from asyncpraw.models.helpers import SubredditHelper
from models.session import Session
from settings import settings
from utils.log import logger
from utils.reddit import AsyncReddit

from handlers.base import BaseHandler


class NewPostsHandler(BaseHandler):
    """Returns new Reddit posts, given a person's account."""

    def _cool(self):
        logger.debug(f'> _cool')
        return 'neat'

    async def get(self):
        """Handle GET request."""
        session: Session = await self.get_session()

        # aio_loop: AbstractEventLoop = asyncio.get_event_loop()
        # logger.debug(f'> loop {aio_loop}')
        # executor: Executor = ThreadPoolExecutor(max_workers=4)
        # # aio_loop.run_until_complete(self._cool())
        # result = await aio_loop.run_in_executor(executor=executor,
        #                                         func=self._cool)
        # logger.debug(f'> result {result}')

        # reddit: AsyncReddit = AsyncReddit(
        reddit = Reddit(
            client_id=settings.get('reddit_client_id'),
            client_secret=settings.get('reddit_secret'),
            refresh_token=session.reddit_credentials.refresh_token,
            user_agent='bigmuseum by u/parsifal'
        )
        # r_museum: SubredditHelper = await reddit.subreddit('museum')
        r_museum: SubredditHelper = await reddit.subreddit('museum')
        logger.debug(f'> museum {dict(r_museum)}')

        self.finish('hello')
