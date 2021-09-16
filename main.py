import logging
import os

import tornado.ioloop
import tornado.options
import tornado.web

from handlers.base import BaseHandler
from handlers.login import LoginHandler, FinishLoginHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class HelloWorldHandler(BaseHandler):
    async def get(self):
        self.write('200')


def make_app() -> tornado.web.Application:
    static_path = os.path.join(os.path.dirname(__file__), 'dist')
    return tornado.web.Application(
        [
            (r'/', HelloWorldHandler),
            (r'/login', LoginHandler),
            (r'/login/complete', FinishLoginHandler),
            # Alias for main app file.
            (r'/app/(.*)', tornado.web.StaticFileHandler, {'path': static_path,
                                                           'default_filename': 'index.html'})
        ],
        debug=True,
        static_path=os.path.join(os.path.dirname(__file__), 'dist'),
        reddit_client_id=os.environ.get('REDDIT_CLIENT_ID', None),
        reddit_secret=os.environ.get('REDDIT_SECRET', 'None'),
        cookie_secret='f3be6678-38cb-4141-ba1b-8691e302407d'
    )


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app: tornado.web.Application = make_app()
    app.listen(8888)
    logger.info('Listening on 8888 ...')
    tornado.ioloop.IOLoop.current().start()
