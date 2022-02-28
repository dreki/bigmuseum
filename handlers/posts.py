"""Holds handlers related to Reddit posts."""
import datetime
from tracemalloc import start
from typing import Dict, Optional, Sequence

from asyncpraw.reddit import Reddit, Submission
from db import AIOEngine, get_engine
from models.curation import Curation
from models.post import Post
from models.user import User
from odmantic.bson import ObjectId
from odmantic.query import desc
from settings import settings
from tornado.web import HTTPError
from utils.date import parse_nl_date
from utils.log import logger
from utils.mongodb import (add_fields, aggregate, aggregate_as_dicts, and_,
                           cond, date_, eq, expr, gt, in_, limit, lookup, match,
                           match_expr, match_expr_eq, not_, not_in, project,
                           replace_with, set_, size, sort, unset, unwind)
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
        """Hide a post on Reddit (Note: This function is untested)."""
        # Get reddit instance
        reddit: Optional[Reddit] = await self.make_reddit_client()
        if not reddit:
            raise HTTPError(status_code=401,
                            reason='Failed to get Reddit client for current user.')
        # Get submission
        submission: Submission = await reddit.submission(id=post_id)
        # Hide submission
        await submission.hide()

    async def _fetch_posts(self, date: str='today 00:00') -> Sequence[Dict]:
        """
        Fetch `Post`s from the database.
        
        :param date: The date to start fetching posts from. Natural language.
        """
        db: AIOEngine = await get_engine()

        start_date: Optional[datetime.datetime] = parse_nl_date(date)
        # end_date: Optional[datetime.datetime] = parse_nl_date(f'{date} +24 hours')
        if not start_date:
            raise ValueError(f'Invalid date: {date}')
        end_date: datetime.datetime = start_date + datetime.timedelta(days=1)

        # Get `Post`s, excluding the `User`'s hidden posts.
        aggregation: Sequence[Dict] = [
            # Only posts from today.
            # TODO: Use user's time zone
            # {'$match': {'$expr': {'$gte': ['$post_created_at', date_('yesterday 00:00')]}}},
            {'$match': {'$expr': {'$gte': ['$post_created_at', date_(start_date)]}}},
            {'$match': {'$expr': {'$lte': ['$post_created_at', date_(end_date)]}}},

            lookup(from_=+User,
                   let={'user_id': self.current_user.id,
                        'post_id': '$_id'},
                   pipeline=[
                       match_expr_eq([f'${+User.id}', '$$user_id']),  # type: ignore
                       replace_with({'hidden_posts': '$hidden_posts'}),
                   ],
                   as_=+User),
            unwind(f'${+User}'),

            # Exclude hidden posts.
            match_expr(not_in(
                [f'${+Post.id}',  # type: ignore
                 f'${+User}.{+User.hidden_posts}'])),  # type: ignore

            # Add matching `Curation`s.
            lookup(from_=+Curation,
                   let={'post_id': '$_id'},
                   pipeline=[
                       match_expr_eq([f'${+Curation.post}', '$$post_id']),  # type: ignore
                   ],
                   as_=f'{+Curation}s'),

            # If there are `curations`, add has_curations to result
            add_fields(has_curations=gt([size(f'${+Curation}s'), 0])),

            # Remove curations and user from result.
            unset(f'{+Curation}s'),
            unset(f'{+User}'),

            # Project `_id` as `id`
            add_fields(id=f'${+Post.id}'),  # type: ignore
            unset(+Post.id),  # type: ignore

            # Limit to 50
            # TODO: Limit based on date, etc.
            # limit(50),
        ]
        logger.debug('> aggregation: ')
        logger.debug(aggregation)
        # from rich.pretty import pprint
        # pprint(aggregation, indent_guides=False)
        result: Sequence[Dict] = await aggregate_as_dicts(engine=db,
                                                          aggregation=aggregation,
                                                          model=Post)
        return result

    async def get(self):
        """Handle GET request."""
        # Get filter from query string.
        filter: Optional[str] = self.get_query_argument('filter', default='new')
        # if not filter or filter not in ['new', 'hot', 'top']:
        if not filter or filter not in ['new']:
            raise HTTPError(status_code=400, reason='Invalid filter.')
        # Get date we should start fetching posts for.
        posts_date: Optional[str] = self.get_query_argument('date', default=None)

        # TODO: Update loading from cache to use date.
        # TODO: Uncomment to enable cache.
        # cached_posts = await self._get_cached_posts()
        # if cached_posts:
        #     await self.json({'items': cached_posts})
        #     return
        logger.debug('> cache missing; fetching posts')
        posts: Sequence[Dict] = await self._fetch_posts()
        await self._set_cached_posts(posts)
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
        if not self.current_user.hidden_posts:
            self.current_user.hidden_posts = []
        self.current_user.hidden_posts.append(post.id)
        await engine.save(self.current_user)

        # Delete any existing posts cache for this User.
        await delete_cache(self._make_cached_posts_key())
        self.finish('')

    async def patch(self, post_id):
        """Update a post."""
        logger.debug(f'> update {post_id}')
        self.finish('')
