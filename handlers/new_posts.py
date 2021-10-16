"""Holds handlers for working with new Reddit posts."""
import asyncio
from asyncio.events import AbstractEventLoop
from concurrent.futures import Executor, ThreadPoolExecutor
from datetime import datetime
from typing import List

# from praw.models.helpers import SubredditHelper
from asyncpraw import Reddit
from asyncpraw.models.helpers import SubredditHelper
from asyncpraw.reddit import Submission, Subreddit
from models.session import Session
from settings import settings
from utils.log import logger
from utils.view_models.post import Post

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
        # r_museum: SubredditHelper = await reddit.subreddit('museum',
        r_museum: Subreddit = await reddit.subreddit('museum')
        #  fetch=True)
        # logger.debug(f'> museum {dict(r_museum)}')
        logger.debug(dir(r_museum))
        # async for post in r_museum.new():
        first: bool = True
        posts: List[Post] = []
        async for submission in r_museum.hot(limit=10):
            submission: Submission
            logger.debug(f'> {submission.title} {submission.url} {submission.created} {submission.created_utc}')
            # logger.debug(dir(post))

            post = Post(title=submission.title,
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
