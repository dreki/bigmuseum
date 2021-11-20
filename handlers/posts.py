"""Holds handlers related to Reddit posts."""
from asyncpraw.reddit import Submission
from utils.log import logger

from handlers.base import BaseHandler


class PostsHandler(BaseHandler):
    """Affords interactions with posts from Reddit."""

    async def delete(self, post_id):
        """Delete a post."""
        logger.debug(f'> hide {post_id}')

        # Get reddit instance
        reddit = await self.make_reddit_client()
        # Get submission
        submission: Submission = await reddit.submission(id=post_id)
        logger.debug(f'> submission: {submission}')
        # Hide submission
        await submission.hide()
        # submission.mod.hide()
        # submission.hide()
        self.finish('')

    # PATCH handler
    async def patch(self, post_id):
        """Update a post."""
        logger.debug(f'> update {post_id}')
        self.finish('')
