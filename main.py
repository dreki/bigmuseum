import logging
import os

import tornado.ioloop
import tornado.options
import tornado.web
from tornado.web import url

import utils.periodic_post_download
from handlers.base import BaseHandler
from handlers.collection_items import CollectionItemsHandler
from handlers.login import FinishLoginHandler, LoginHandler
from handlers.new_posts import NewPostsHandler
from handlers.posts import PostsHandler
from settings import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

settings.update({
    'debug': True,
    'reddit_client_id': os.environ.get('REDDIT_CLIENT_ID', None),
    'reddit_secret': os.environ.get('REDDIT_SECRET', 'None'),
    'mongo_host': os.environ.get('MONGO_HOST', 'None'),
    'mongo_user': os.environ.get('MONGO_USER', 'None'),
    'mongo_password': os.environ.get('MONGO_PASSWORD', 'None'),
    'mongo_db': os.environ.get('MONGO_DB', 'None'),
    'cookie_secret': 'f3be6678-38cb-4141-ba1b-8691e302407d'
})

# Update `settings` with what's in the environment
# settings.update(os.environ)
# # Lower-case all keys in `settings`
# settings = {k.lower(): v for k, v in settings.items()}


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
            (r'/api/posts', PostsHandler),
            (r'/api/posts/(?P<post_id>[^/]+)', PostsHandler),
            (r'/api/collection/items', CollectionItemsHandler),
            # Alias for main app file.
            # (
            url(
                r'/app/(.*)',
                tornado.web.StaticFileHandler,
                {
                    'path': static_path,
                    'default_filename': 'index.html',
                },
                name='app'
            )
        ],
        static_path=os.path.join(os.path.dirname(__file__), 'dist'),
        autoreload=True,
        **settings
    )


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app: tornado.web.Application = make_app()
    app.listen(8888)
    logger.info('Listening on 8888 ...')
    tornado.ioloop.IOLoop.current().add_callback(utils.periodic_post_download.start)
    tornado.ioloop.IOLoop.current().start()
