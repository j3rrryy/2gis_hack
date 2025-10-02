from cashews import cache
from sqlalchemy.ext.asyncio import AsyncSession

from dto import request as request_dto
from dto import response as response_dto
from enums.enums import CacheKeys
from repository import ExampleRepository


class ExampleService:
    @staticmethod
    async def create_example(
        data: request_dto.CreateRequestDTO, session: AsyncSession
    ) -> str:
        # example of data modification
        data = data.replace(name=data.name + "-created")
        example_id = await ExampleRepository.create_example(data, session)

        # example of cache invalidation
        await cache.delete(CacheKeys.EXAMPLES.value)
        return example_id

    @staticmethod
    async def list_examples(
        session: AsyncSession,
    ) -> list[response_dto.ExampleResponseDTO]:
        # example of caching
        if cached := await cache.get(CacheKeys.EXAMPLES.value):
            return cached

        examples = await ExampleRepository.list_examples(session)
        await cache.set(CacheKeys.EXAMPLES.value, examples, 3600)  # 1h
        return examples

    @staticmethod
    async def get_example(
        example_id: str, session: AsyncSession
    ) -> response_dto.ExampleResponseDTO:
        # example of caching
        cache_key = f"{CacheKeys.EXAMPLE.value}{example_id}"
        if cached := await cache.get(cache_key):
            return cached

        example = await ExampleRepository.get_example(example_id, session)
        await cache.set(cache_key, example, 3600)  # 1h
        return example

    @classmethod
    async def update_example(
        cls, example_id: str, data: request_dto.UpdateRequestDTO, session: AsyncSession
    ) -> response_dto.ExampleResponseDTO:
        # example of data modification
        if data.name:
            data = data.replace(name=data.name + "-updated")

        example = await ExampleRepository.update_example(example_id, data, session)
        await cls._invalidate_example_cache(example_id)
        return example

    @classmethod
    async def delete_example(cls, example_id: str, session: AsyncSession) -> None:
        await ExampleRepository.delete_example(example_id, session)
        await cls._invalidate_example_cache(example_id)

    @staticmethod
    async def _invalidate_example_cache(example_id: str) -> None:
        # example of cache invalidation
        await cache.delete(CacheKeys.EXAMPLES.value)
        await cache.delete(f"{CacheKeys.EXAMPLE.value}{example_id}")
