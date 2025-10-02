from cashews import cache
from sqlalchemy.ext.asyncio import AsyncSession

from dto import request as request_dto
from dto import response as response_dto
from enums.enums import CacheKeys
from repository import ExampleRepository


class ExampleService:
    @staticmethod
    async def create(data: request_dto.CreateRequestDTO, session: AsyncSession) -> str:
        data = data.replace(name=data.name + "-created")  # example of data modification
        example_id = await ExampleRepository.create(data, session)
        await cache.delete(CacheKeys.EXAMPLES.value)  # example of cache invalidation
        return example_id

    @staticmethod
    async def read(session: AsyncSession) -> list[response_dto.ReadResponseDTO]:
        # example of caching
        if cached := await cache.get(CacheKeys.EXAMPLES.value):
            return cached

        examples = await ExampleRepository.read(session)
        await cache.set(CacheKeys.EXAMPLES.value, examples, 3600)
        return examples
