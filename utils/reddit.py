"""Provides an asyncio-compatible Reddit class."""
import asyncio
import inspect
from asyncio.events import AbstractEventLoop
from concurrent.futures import Executor, Future, ThreadPoolExecutor
from functools import partial
from typing import Any, Awaitable, Optional, Union

import praw

from utils.log import logger


class AsyncReddit(praw.Reddit):
    """An asyncio-enabled `praw.Reddit` client."""

    _io_loop: Optional[AbstractEventLoop] = None
    _executor: Optional[Executor] = None

    @classmethod
    @property
    def io_loop(cls) -> AbstractEventLoop:
        """Return a shared reference to the currently-running asyncio event loop."""
        if not cls._io_loop:
            cls._io_loop: AbstractEventLoop = asyncio.get_event_loop()
        return cls._io_loop

    @classmethod
    @property
    def executor(cls) -> Executor:
        """Return a shared Executor."""
        if not cls._executor:
            cls._executor: Executor = ThreadPoolExecutor(max_workers=4)
        return cls._executor

    # @classmethod
    # def __getattribute__(self, name: str) -> Union[Awaitable, Any, None]:
    #     """Make callable methods async-compatible."""
    #     # return super().__getattribute__(name)
    #     original_attribute = super().__getattribute__(name)
    #     if not callable(original_attribute):
    #         return original_attribute
    #     return self.io_loop.run_in_executor(
    #         executor=self.executor,
    #         func=original_attribute
    #     )
    def __getattribute__(self, name: str) -> Any:
        original_attribute = super().__getattribute__(name)
        logger.debug(f'> __getattribute__ {getattr(original_attribute, "__name__", None)}')
        logger.debug(f'  > {original_attribute}')
        # if getattr(original_attribute, '__name__', None) not in ('subreddit',):
        #     return original_attribute
        if not callable(original_attribute):
            return original_attribute
        if inspect.isclass(original_attribute):
            return original_attribute
        # if str(original_attribute).startswith('_'):
        if getattr(original_attribute, '__name__', '').startswith('_'):
            return original_attribute

        def _run_in_thread(attribute, *args, **kwargs) -> Future:
            """
            Run the originally-referenced method in an
            asyncio thread.
            """
            return self.io_loop.run_in_executor(
                executor=self.executor,
                func=partial(attribute, *args, **kwargs)
            )
        return partial(_run_in_thread, original_attribute)
