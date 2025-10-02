from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from dto import request as request_dto

from .models import Example


class ExampleRepository:
    @staticmethod
    async def create(data: request_dto.CreateRequestDTO, session: AsyncSession) -> str:
        new_example = Example(name=data.name)
        session.add(new_example)

        try:
            await session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Example with this name already exists",
            )

        await session.refresh(new_example)
        return new_example.example_id
