import tornado.ioloop
import tornado.options
import tornado.web
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class HelloWorldHandler(tornado.web.RequestHandler):
    async def get(self):
        self.write('200')


def make_app() -> tornado.web.Application:
    return tornado.web.Application(
        [
            (r'/', HelloWorldHandler)
        ],
        debug=True
    )


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app: tornado.web.Application = make_app()
    app.listen(8888)
    logger.info('Listening on 8888 ...')
    tornado.ioloop.IOLoop.current().start()
