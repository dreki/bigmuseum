from typing import Any, Awaitable, Optional
from uuid import uuid4

import tornado.web
from db import AIOEngine, get_engine
from models.session import Session
from tornado import httputil


class BaseHandler(tornado.web.RequestHandler):
    """Holds common functionality for all of our handlers."""

    def __init__(self,
                 application: tornado.web.Application,
                 request: httputil.HTTPServerRequest,
                 **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        self._session: Optional[str] = None
        # self._reddit_credentials: Optional[RedditCredentials] = None

    async def prepare(self) -> Optional[Awaitable[None]]:
        """Perform common tasks for all requests."""
        if not self.get_secure_cookie('session'):
            self.set_secure_cookie('session', str(uuid4()))
        self._session = self.get_secure_cookie('session').decode('utf-8')
        return super().prepare()

    # @property
    # def session(self) -> Optional[str]:
    #     """Return the current request's session ID."""
    #     return self._session

    async def get_session(self, key: Optional[str] = None) -> Session:
        """Get the current user's `Session` record."""
        engine: AIOEngine = await get_engine()
        if not key:
            key = self._session
        session: Session = await engine.find_one(Session,
                                                 Session.key == key)
        # Create `Session` record if it's missing.
        if not session:
            session: Session = Session(key=key)
            await engine.save(session)
        return session

    # @property
    # def reddit_credentials(self) -> Optional[RedditCredentials]:
    #     """Return the currently-saved Reddit credentials, if present."""
    #     return self._reddit_credentials

    # @reddit_credentials.setter
    # def reddit_credentials(self, val: RedditCredentials):
    #     """Set some saved Reddit credentials."""
    #     self._reddit_credentials = val
