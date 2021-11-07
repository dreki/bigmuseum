"""Holds handlers related to Reddit posts."""
from utils.log import logger

from handlers.base import BaseHandler


class PostsHandler(BaseHandler):
    """Affords interactions with posts from Reddit."""

    async def delete(self, post_id):
        """Delete a post."""
        logger.debug(f'> hide {post_id}')
        self.finish('')
