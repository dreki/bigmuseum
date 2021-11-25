
import atexit
import logging
from typing import Optional

logger: logging.Logger


def init():
    """Initialize global logging."""
    global logger
    logger = logging.getLogger('bigmuseum')
    logger.setLevel(logging.DEBUG)
    atexit.register(logging.shutdown)
    return logger


init()
