from typing import Awaitable, Optional
from uuid import uuid4

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """Holds common functionality for all of our handlers."""

    async def prepare(self) -> Optional[Awaitable[None]]:
        """Perform common tasks for all requests."""
        if not self.get_secure_cookie('session'):
            self.set_secure_cookie('session', str(uuid4()))
        self._session: str = self.get_secure_cookie('session').decode('utf-8')
        return super().prepare()

    @property
    def session(self) -> Optional[str]:
        """Return the current request's session ID."""
        return self._session
