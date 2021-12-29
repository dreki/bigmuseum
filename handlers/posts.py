"""Holds handlers related to Reddit posts."""
from typing import Optional
from asyncpraw.reddit import Reddit, Submission
from db import get_engine, AIOEngine
from models.post import Post
from odmantic.bson import ObjectId
from tornado.web import HTTPError
from utils.log import logger
from utils.redis import delete_cache

from handlers.base import BaseHandler


class PostsHandler(BaseHandler):
    """Affords interactions with posts from Reddit."""

    async def delete(self, post_id):
        """Delete a post."""
        logger.debug(f'> hide {post_id}')

        # TODO: Uncomment if we want to hide on Reddit.
        # Remember to look up Reddit post ID from `Post`.
        #
        # Get reddit instance
        # reddit: Optional[Reddit] = await self.make_reddit_client()
        # if not reddit:
        #     raise HTTPError(status_code=401,
        #                     reason='Failed to get Reddit client for current user.')
        # Get submission
        # submission: Submission = await reddit.submission(id=post_id)
        # logger.debug(f'> submission: {submission}')
        # # Hide submission
        # await submission.hide()

        # Record hide in `User` document.
        engine: AIOEngine = await get_engine()
        # post: Post = await self.db().find_one(Post, Post.id == ObjectId(post_id))
        post: Optional[Post] = await engine.find_one(Post, Post.id == ObjectId(post_id))
        if not post:
            raise HTTPError(status_code=400, reason='Post not found.')
        logger.debug(f'> current user:')
        logger.debug(self.current_user)
        # self.current_user.hidden_posts.add(post.id)
        # self.current_user.add_hidden_post(post.id)
        if not self.current_user.hidden_posts:
            self.current_user.hidden_posts = []
        self.current_user.hidden_posts.append(post.id)
        await engine.save(self.current_user)

        # Delete any existing posts cache for this User.
        await delete_cache(self._make_cached_posts_key())

        # await self.current_user.hidden_posts.append(ObjectId(post_id))

        self.finish('')

    # PATCH handler
    async def patch(self, post_id):
        """Update a post."""
        logger.debug(f'> update {post_id}')
        self.finish('')
