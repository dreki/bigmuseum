
import atexit
import logging
from typing import Optional
from rich.console import Console
from rich.logging import RichHandler

logger: logging.Logger
# logger: Console


def init():
    """Initialize global logging."""
    global logger
    # log_console: Console = Console(soft_wrap=True, color_system='truecolor')
    log_console: Console = Console(color_system='truecolor', tab_size=4,
                                   width=120)
    logging.basicConfig(level='NOTSET',
                        format='%(message)s',
                        datefmt='[%X]',
                        # handlers=[RichHandler(markup=True,
                        #                       console=log_console)])
                        handlers=[RichHandler(markup=True,
                                              rich_tracebacks=True,
                                              console=log_console)])
    logger = logging.getLogger('rich')
    # logger = log_console
    # return logger

    # logger = logging.getLogger('bigmuseum')
    logger.setLevel(logging.DEBUG)
    atexit.register(logging.shutdown)
    return logger


init()
