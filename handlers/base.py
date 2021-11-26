"""Holds shared `RequestHandler` functionality."""
from __future__ import annotations
import datetime
import json
from typing import Any, Awaitable, Dict, Optional, Type
from uuid import uuid4

import humps
import tornado.web
from asyncpraw.reddit import Reddit
from tornado import httputil

from db import AIOEngine, get_engine
from models.session import Session
from utils.log import logger
from utils.reddit import get_reddit


class BaseHandler(tornado.web.RequestHandler):
    """Holds common functionality for all of our handlers."""

    def __init__(self,
                 application: tornado.web.Application,
                 request: httputil.HTTPServerRequest,
                 **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        self._session: Optional[str] = None

    async def prepare(self) -> Optional[Awaitable[None]]:
        """Perform common tasks for all requests."""
        # Print out cookie
        if not self.get_secure_cookie('session'):
            self.set_secure_cookie('session', str(uuid4()))
        self._session = self.get_secure_cookie('session').decode('utf-8')
        return super().prepare()

    async def get_session(self, key: Optional[str] = None) -> Session:
        """Get the current user's `Session` record."""
        engine: AIOEngine = await get_engine()
        if not key:
            key = self._session
        session: Session = await engine.find_one(Session,
                                                 Session.key == key)
        # Create `Session` record if it's missing.
        logger.debug(f'> session: {session}')
        if not session:
            session: Session = Session(key=key)
            await engine.save(session)
        return session

    def _encode_as_json(obj: Any) -> str:
        if isinstance(obj, datetime.datetime):
            obj: datetime.datetime
            return obj.isoformat()
        raise TypeError(f'Unexpected type {type(obj)}.')

    async def json(self, payload: Dict) -> None:
        """Send a JSON response."""
        self.set_header('Content-Type', 'application/json')
        payload = humps.camelize(payload)
        return self.finish(json.dumps(payload, default=str))

    async def get_json_body(self) -> Dict:
        """Get the JSON body of the request."""
        j: Dict = json.loads(self.request.body.decode('utf-8'))
        j = humps.decamelize(j)
        return j

    async def make_reddit_client(self) -> Reddit:
        """Create a `Reddit` client."""
        session: Session = await self.get_session()
        refresh_token = session.reddit_credentials.refresh_token
        reddit = await get_reddit(refresh_token)
        return reddit
