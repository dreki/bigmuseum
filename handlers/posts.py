"""Holds handlers related to Reddit posts."""
from os import pipe
from typing import Dict, List, Optional, Sequence

from asyncpraw.reddit import Reddit, Submission
from odmantic.query import desc
from db import AIOEngine, get_engine
from models.curation import Curation
from models.post import Post
from models.user import User
from odmantic.bson import ObjectId
from settings import settings
from tornado.web import HTTPError
from utils.log import logger
from utils.mongodb import (aggregate, aggregate_as_dicts, and_, eq, expr, in_,
                           limit, lookup, match, project, replace_with, sort,
                           unwind, cond, gt, size, set_, not_, unset, match_expr)
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

    # async def _set_cached_posts(self, posts: Sequence[Post]) -> None:
    async def _set_cached_posts(self, posts: Sequence[Dict]) -> None:
        """Set cached posts."""
        cache_key: str = self._make_cached_posts_key()
        if not settings.get('new_posts_cache_expiration_seconds'):
            raise ValueError(
                'NEW_POSTS_CACHE_EXPIRATION_SECONDS must be set in environment.')
        await set_cache(cache_key,
                        # [p.dict() for p in posts],
                        posts,
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

    # async def _fetch_posts(self) -> Sequence[Post]:
    async def _fetch_posts(self) -> Sequence[Dict]:
        """Fetch `Post`s from the database."""
        db: AIOEngine = await get_engine()

        # Get `Post`s, excluding the `User`'s hidden posts.
        # aggregation: Sequence[Dict] = [
        #     lookup(
        #         from_=+User,
        #         let={'user_id': self.current_user.id},
        #         pipeline=[
        #             match(expr({+User.id: '$$user_id'})),  # type: ignore
        #             replace_with({'hidden_posts': '$hidden_posts'}),
        #         ],
        #         as_=+User
        #     ),
        #     unwind(f'${+User}'),

        #     set_(hidden_posts=f'${+User}.{+User.hidden_posts}'),  # type: ignore
        #     unset(+User),

        #     # Exclude hidden posts.
        #     match(expr(not_(in_([++Post.id,  # type: ignore
        #                          ++User.hidden_posts])))),  # type: ignore

        #     # Limit to 200 posts.
        #     # limit(200),
        #     limit(40),
        # ]
        aggregation: Sequence[Dict] = [
            lookup(from_=+User,
                   let={'user_id': self.current_user.id,
                        'post_id': '$_id'},
                   pipeline=[
                       #    match_expr(f'{+User.id}'=$$user_id),
                       match_expr({f'{+User.id}': '$$user_id'}),  # type: ignore
                       replace_with({'hidden_posts': '$hidden_posts'}),
                   ],
                   as_=+User),
            unwind(f'${+User}'),
        ]
        logger.debug('> aggregation:')
        logger.debug(aggregation)
        # posts: Sequence[Post] = await aggregate(engine=db,
        #                                         aggregation=aggregation,
        #                                         model=Post)
        # return [p.dict() for p in posts]

        # return await aggregate_as_dicts(engine=db,
        #                                 aggregation=aggregation,
        #                                 model=Post)
        result: Sequence[Dict] = await aggregate_as_dicts(engine=db,
                                                          aggregation=aggregation,
                                                          model=Post)
        logger.debug('> result:')
        logger.debug(result)
        return []

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
        # posts: Sequence[Post] = await self._fetch_posts()
        posts: Sequence[Dict] = await self._fetch_posts()
        await self._set_cached_posts(posts)
        logger.debug('> returning posts')
        # await self.json({'items': [p.dict() for p in posts]})
        await self.json({'items': posts})

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
