import httpx
from db import AIOEngine, get_engine
from models.session import RedditCredentials, Session

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
        async with httpx.AsyncClient() as http:
            response: httpx.Response = \
                await http.post('https://www.reddit.com/api/v1/access_token',
                                auth=(self.application.settings.get('reddit_client_id'),
                                      self.application.settings.get('reddit_secret')),
                                data={'grant_type': 'authorization_code',
                                      'code': code,
                                      'redirect_uri': 'http://localhost:8888/login/complete'})
            credentials: RedditCredentials = RedditCredentials.parse_obj(response.json())
            session.reddit_credentials = credentials
            await engine.save(session)
            self._reddit_credentials = credentials
        self.redirect(url=self.reverse_url('app', ''))

    async def post(self):
        self.finish('POST')
