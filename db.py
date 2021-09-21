from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from settings import settings

engine: Optional[AIOEngine] = None


async def get_engine() -> AIOEngine:
    global engine
    if engine:
        return engine
    connection_string = (f'mongodb://'
                         f'{settings.get("mongo_user")}'
                         f':{settings.get("mongo_password")}'
                         f'@{settings.get("mongo_host")}/')
    print(f'> connection_string {connection_string}')
    client: AsyncIOMotorClient = AsyncIOMotorClient(
        connection_string
    )
    engine = AIOEngine(motor_client=client,
                       database=settings.get('mongo_db'))
    return engine
