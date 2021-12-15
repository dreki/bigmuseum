"""Holds code for items in someone's collection."""
from typing import Dict
from asyncpraw.reddit import Reddit, Redditor
from models.session import Session
from utils.log import logger

from handlers.base import BaseHandler


class CollectionItemsHandler(BaseHandler):
    """Represents reading and changing items in a person's collection."""

    async def post(self):
        """Handle POST request."""
        session: Session = await self.get_session()
        logger.debug(f'> session:')
        logger.debug(session)
        logger.debug('> a dict:')
        logger.debug({'first': 1, 'second': 2})
        reddit: Reddit = await self.make_reddit_client()
        # logger.debug(dir(reddit.user))
        # logger.debug(dir(await reddit.user.me()))
        redditor: Redditor = await reddit.user.me()
        logger.debug(f'> {redditor.name} ({redditor.id})')
        # post_id: str = self.get_argument('post_id')
        # logger.debug(f'> save {post_id}')

        # logger.debug(self.get_body_argument('post_id'))

        # Get JSON body of request
        # logger.debug(self.request.body)
        json_body: Dict = await self.get_json_body()
        logger.debug(f'> json_body: {json_body}')
        post_id: str = json_body.get('post_id')
        logger.debug(f'> save {post_id}')
        await self.finish('')
