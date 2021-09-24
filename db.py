from typing import List, Optional, Sequence

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from models.model import ModelType
from settings import settings

engine: Optional[AIOEngine] = None


class TimestampingAIOEngine(AIOEngine):
    async def save(self, instance: ModelType) -> ModelType:
        # instance = self._set_timestamps()
        # await self._call_pre_save(instance)
        await instance.pre_save()
        return await super().save(instance)

    async def save_all(self, instances: Sequence[ModelType]) -> List[ModelType]:
        [await i.pre_save() for i in instances]
        return await super().save_all(instances)


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
    # engine = AIOEngine(motor_client=client,
    #                    database=settings.get('mongo_db'))
    engine = TimestampingAIOEngine(
        motor_client=client,
        database=settings.get('mongo_db')
    )
    return engine


# async def cool():
#     engine: AIOEngine = await get_engine()
#     await engine.find
