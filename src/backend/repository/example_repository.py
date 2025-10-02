from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from dto import request as request_dto
from dto import response as response_dto

from .models import Example


class ExampleRepository:
    @staticmethod
    async def create_example(
        data: request_dto.CreateRequestDTO, session: AsyncSession
    ) -> str:
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

    @staticmethod
    async def list_examples(
        session: AsyncSession,
    ) -> list[response_dto.ExampleResponseDTO]:
        examples = (await session.execute(select(Example))).scalars().all()
        return [
            response_dto.ExampleResponseDTO.from_model(example) for example in examples
        ]

    @staticmethod
    async def get_example(
        example_id: str, session: AsyncSession
    ) -> response_dto.ExampleResponseDTO:
        example = await session.get(Example, example_id)
        if not example:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Example not found",
            )
        return response_dto.ExampleResponseDTO.from_model(example)

    @staticmethod
    async def update_example(
        example_id: str, data: request_dto.UpdateRequestDTO, session: AsyncSession
    ) -> response_dto.ExampleResponseDTO:
        example = await session.get(Example, example_id)
        if not example:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Example not found",
            )

        for field in data.__dataclass_fields__:
            value = getattr(data, field)
            if value is not None:
                setattr(example, field, value)

        try:
            await session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Example with this name already exists",
            )
        return response_dto.ExampleResponseDTO.from_model(example)

    @staticmethod
    async def delete_example(example_id: str, session: AsyncSession) -> None:
        deleted_rows = (
            await session.execute(
                delete(Example).where(Example.example_id == example_id)
            )
        ).rowcount
        if not deleted_rows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Example not found",
            )
        await session.commit()
