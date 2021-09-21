
import atexit
import logging
from typing import Optional

logger: Optional[logging.Logger] = None


def init():
    """Initialize global logging."""
    global logger
    logger = logging.getLogger('bigmuseum')
    logger.setLevel(logging.DEBUG)
    atexit.register(logging.shutdown)
    return logger


init()
