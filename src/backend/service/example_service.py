from sqlalchemy.ext.asyncio import AsyncSession

from dto import request as request_dto
from repository import ExampleRepository


class ExampleService:
    @staticmethod
    async def create(data: request_dto.CreateRequestDTO, session: AsyncSession) -> str:
        data = data.replace(
            name=data.name + "-modificated"
        )  # example of data modification
        example_id = await ExampleRepository.create(data, session)
        return example_id
