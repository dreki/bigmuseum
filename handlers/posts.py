"""Holds handlers related to Reddit posts."""
from typing import Dict, List, Optional, Sequence

from asyncpraw.reddit import Reddit, Submission
from db import AIOEngine, get_engine
from models.post import Post
from models.user import User
from odmantic.bson import ObjectId
from settings import settings
from tornado.web import HTTPError
from utils.log import logger
from utils.mongodb import (aggregate, and_, eq, in_, lookup, match, project,
                           replace_with, sort, unwind)
from utils.redis import delete_cache, get_cache, set_cache

from handlers.base import BaseHandler


class PostsHandler(BaseHandler):
    """Affords interactions with posts from Reddit."""

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
            raise ValueError(
                'NEW_POSTS_CACHE_EXPIRATION_SECONDS must be set in environment.')
        await set_cache(cache_key,
                        [p.dict() for p in posts],
                        expire_seconds=settings.get('new_posts_cache_expiration_seconds'))

    async def _hide_on_reddit(self, post_id: str):
        """Hide a post on Reddit. (Note: This function is untested.)"""
        # Get reddit instance
        reddit: Optional[Reddit] = await self.make_reddit_client()
        if not reddit:
            raise HTTPError(status_code=401,
                            reason='Failed to get Reddit client for current user.')
        # Get submission
        submission: Submission = await reddit.submission(id=post_id)
        # Hide submission
        await submission.hide()

    async def _fetch_posts(self) -> Sequence[Post]:
        """Fetch `Post`s from the database."""
        db: AIOEngine = await get_engine()
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
            project(hidden=False),
            sort(Post.post_created_at.desc())  # type: ignore
        ]
        posts: Sequence[Post] = await aggregate(engine=db,
                                                aggregation=aggregation,
                                                model=Post)
        return posts

    async def get(self):
        """Handle GET request."""
        # Get filter from query string.
        filter: Optional[str] = self.get_query_argument('filter', default='new')
        # if not filter or filter not in ['new', 'hot', 'top']:
        if not filter or filter not in ['new']:
            raise HTTPError(status_code=400, reason='Invalid filter.')

        cached_posts = await self._get_cached_posts()
        if cached_posts:
            await self.json({'items': cached_posts})
            return
        logger.debug('> cache missing; fetching posts')
        posts: Sequence[Post] = await self._fetch_posts()
        await self._set_cached_posts(posts)
        logger.debug('> returning posts')
        await self.json({'items': [p.dict() for p in posts]})

    async def delete(self, post_id):
        """Delete a post."""
        logger.debug(f'> hide {post_id}')

        # TODO: Uncomment if we want to hide on Reddit.
        # await self._hide_on_reddit(post_id=post_id)

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

    async def patch(self, post_id):
        """Update a post."""
        logger.debug(f'> update {post_id}')
        self.finish('')
