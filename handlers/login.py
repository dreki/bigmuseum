from typing import Optional
import httpx
# from asyncpraw.models import User
from asyncpraw.models import Redditor
from asyncpraw.reddit import Reddit
from db import AIOEngine, get_engine
from models.session import RedditCredentials, Session
from models.user import User
from tornado.web import HTTPError
from utils.log import logger
from settings import settings

from handlers.base import BaseHandler


class LoginHandler(BaseHandler):
    """Handles initiating Reddit login."""
    async def get(self):
        session: Session = await self.get_session()
        url: str = (f'https://www.reddit.com/api/v1/authorize'
                    f'?client_id=McdKsmpEBaZYVv69oAMS6Q'
                    f'&response_type=code'
                    f'&state={session.key}'
                    f'&redirect_uri=http://localhost:8888/login/complete'
                    f'&duration=permanent'
                    f'&scope=history,identity,vote,read,report')
        self.redirect(url=url, permanent=False)


class FinishLoginHandler(BaseHandler):
    async def get(self):
        # Get the engine here, in case it fails.
        engine: AIOEngine = await get_engine()
        session: Session = await self.get_session(key=self.get_argument('state'))
        # Get access token, so we can access the Reddit API.
        code: str = self.get_argument('code')

        # Get Reddit API credentials, erroring if they're missing.
        reddit_client_id: str = settings.get('reddit_client_id', '')
        reddit_secret: str = settings.get('reddit_secret', '')
        if not reddit_client_id or not reddit_secret:
            raise HTTPError(500, 'Reddit client ID or secret not set.')

        # Get credentials to use with the Reddit API.
        async with httpx.AsyncClient() as http:
            response: httpx.Response = \
                await http.post('https://www.reddit.com/api/v1/access_token',
                                auth=(reddit_client_id, reddit_secret),
                                data={'grant_type': 'authorization_code',
                                      'code': code,
                                      'redirect_uri': 'http://localhost:8888/login/complete'})
            credentials: RedditCredentials = RedditCredentials.parse_obj(response.json())
            session.reddit_credentials = credentials
            await engine.save(session)

            # # Get Reddit user's ID
            # reddit: Reddit = await self.make_reddit_client()

            # logger.debug(await reddit.user.me())
            # current_redditor: Optional[Redditor] = await reddit.user.me()
            # if not current_redditor:
            #     raise HTTPError(status_code=500, reason='Failed to get Redditor information.')
            # reddit_username: str = current_redditor.name
            # # Find a User if it exists.
            # user: Optional[User] = await engine.find_one(User, User.username == reddit_username)
            # if not user:
            #     user = User(username=reddit_username)
            # await engine.save(user)

            # if user:
            #     user.reddit_credentials = credentials
            # else:

            self._reddit_credentials = credentials
        self.redirect(url=self.reverse_url('app', ''))

    async def post(self):
        self.finish('POST')
