"""Provides an asyncio-compatible Reddit class."""
import asyncio
from asyncio.events import AbstractEventLoop
from concurrent.futures import Executor, ThreadPoolExecutor
from typing import Any, Awaitable, Optional, Union

import praw

executor: Executor = ThreadPoolExecutor(max_workers=4)


class AsyncReddit(praw.Reddit):
    """An asyncio-enabled `praw.Reddit` client."""

    io_loop: Optional[AbstractEventLoop] = None

    @classmethod
    @property
    def io_loop(cls):
        """Return a shared reference to the currently-running asyncio event loop."""
        if not cls.io_loop:
            cls.io_loop = asyncio.get_event_loop()
        return cls.io_loop

    def __getattribute__(self, name: str) -> Union[Awaitable, Any, None]:
        """Make callable methods async-compatible."""
        return super().__getattribute__(name)
