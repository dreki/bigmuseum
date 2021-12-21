"""Holds code for items in someone's collection."""
from typing import Dict, Optional
from asyncpraw.reddit import Reddit, Redditor
from db import get_engine
from models.curation import Curation
from models.post import Post
from models.session import Session
from odmantic.bson import ObjectId
from odmantic.engine import AIOEngine
from tornado.web import HTTPError
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
        reddit: Optional[Reddit] = await self.make_reddit_client()
        if not reddit:
            raise HTTPError(status_code=401,
                            reason='Failed to get Reddit client for current user.')
        # logger.debug(dir(reddit.user))
        # logger.debug(dir(await reddit.user.me()))
        redditor: Optional[Redditor] = await reddit.user.me()
        if not redditor:
            raise
        logger.debug(f'> {redditor.name} ({redditor.id})')
        # post_id: str = self.get_argument('post_id')
        # logger.debug(f'> save {post_id}')

        # logger.debug(self.get_body_argument('post_id'))

        # Get JSON body of request
        # logger.debug(self.request.body)
        json_body: Dict = await self.get_json_body()
        logger.debug(f'> json_body: {json_body}')
        post_id: Optional[str] = json_body.get('post_id')
        if not post_id:
            raise HTTPError(status_code=400, reason='Missing post_id.')
        db: AIOEngine = await get_engine()
        post: Optional[Post] = await db.find_one(Post, Post.id == ObjectId(post_id))
        if not post:
            logger.debug(f'> failed to find post: {post_id}')
            raise HTTPError(status_code=400, reason='Post not found.')
        logger.debug(f'> save {post_id}')
        # Save the `Post` to the user's collection.
        curation: Curation = Curation(user=self.current_user,
                                      post=post)
        logger.debug(f'> curation:')
        logger.debug(curation)
        # await self.finish('')
        await reddit.close()
        await db.save(curation)
        await self.json({'success': True})
