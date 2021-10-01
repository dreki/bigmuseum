import asyncio
from asyncio.events import AbstractEventLoop
from concurrent.futures import Executor, ThreadPoolExecutor

from models.session import Session
from utils.log import logger

from handlers.base import BaseHandler


class NewPostsHandler(BaseHandler):
    def _cool(self):
        logger.debug(f'> _cool')
        return 'neat'

    async def get(self):
        session: Session = await self.get_session()

        aio_loop: AbstractEventLoop = asyncio.get_event_loop()
        logger.debug(f'> loop {aio_loop}')
        executor: Executor = ThreadPoolExecutor(max_workers=4)
        # aio_loop.run_until_complete(self._cool())
        result = await aio_loop.run_in_executor(executor=executor,
                                                func=self._cool)
        logger.debug(f'> result {result}')
        self.finish('hello')
