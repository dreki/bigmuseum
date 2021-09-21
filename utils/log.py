
import logging
import sys
from typing import Optional
import atexit

import tornado.log

logger: Optional[logging.Logger] = None


def init():
    """Initialize global logging."""
    global logger
    # if logger:
    #     return logger
    # logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('bigmuseum')
    logger.setLevel(logging.DEBUG)

    atexit.register(logging.shutdown)

    # logger.handlers[0].setFormatter(tornado.log.LogFormatter())

    # handler = logging.StreamHandler(stream=sys.stdout)
    # handler.setFormatter(tornado.log.LogFormatter())
    # handler.setLevel(logging.DEBUG)
    # logger.addHandler(handler)
    # print(f'> LOGGER {logger}')
    return logger


init()
