import tornado.web
from utils.log import logger
import httpx
from handlers.base import BaseHandler
from utils.reddit.models import RedditCredentials


class LoginHandler(BaseHandler):
    """Handles initiating Reddit login."""
    async def get(self):
        # self.write('200')
        url: str = (f'https://www.reddit.com/api/v1/authorize'
                    f'?client_id=McdKsmpEBaZYVv69oAMS6Q'
                    f'&response_type=code'
                    # f'&state=RANDOM_STRING'
                    f'&state={self.session}'
                    f'&redirect_uri=http://localhost:8888/login/complete'
                    f'&duration=permanent'
                    f'&scope=history,identity,vote,read,report')
        self.redirect(url=url, permanent=False)


class FinishLoginHandler(BaseHandler):
    async def get(self):
        # Get access token, so we can access the Reddit API.
        state: str = self.get_argument('state')
        code: str = self.get_argument('code')
        async with httpx.AsyncClient() as http:
            response: httpx.Response = \
                await http.post('https://www.reddit.com/api/v1/access_token',
                                # headers={'Auth'},
                                auth=(self.application.settings.get('reddit_client_id'),
                                      self.application.settings.get('reddit_secret')),
                                data={'grant_type': 'authorization_code',
                                      'code': code,
                                      'redirect_uri': 'http://localhost:8888/login/complete'})
            credentials: RedditCredentials = RedditCredentials.from_json(
                response.json())
            logger.debug(f'> credentials {credentials}')
            logger.debug(f'> state {state}')
            self._reddit_credentials = credentials
        self.finish('GET')

    async def post(self):
        self.finish('POST')
