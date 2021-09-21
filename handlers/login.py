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
        # self.get_query_argument()
        # logger.debug(f'GET {self.get_}')
        # logger.debug(f'> GET {self.request.query_arguments}')

        # logger.debug(
        #     f'> GET {self.get_argument("state")} {self.get_argument("code")}')

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
            logger.debug(f'> response:')
            logger.debug(response)
            logger.debug(response.json())
            credentials: RedditCredentials = RedditCredentials.from_json(
                response.json())
            logger.debug(credentials)
            # self.set_reddit_credentials(response.json())
            self._reddit_credentials = credentials
        # logger.info('info')
        # logger.debug('debug')
        self.finish('GET')

    async def post(self):
        self.finish('POST')
