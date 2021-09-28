from models.session import Session
from handlers.base import BaseHandler


class NewPostHandler(BaseHandler):
    async def get(self):
        session: Session = await self.get_session()
        self.finish('hello')
