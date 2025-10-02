from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from di import SessionManager
from dto import request as request_dto
from schemas import (
    CreateRequestSchema,
    CreateResponseSchema,
    ExampleSchema,
    UpdateSchema,
)
from service import ExampleService

router = APIRouter(prefix="/example", tags=["example"])


@router.post("/", status_code=201, response_model=CreateResponseSchema)
async def create_example(
    data: CreateRequestSchema,
    session: AsyncSession = Depends(SessionManager.session_factory),
) -> CreateResponseSchema:
    dto = request_dto.CreateRequestDTO.from_schema(data)
    example_id = await ExampleService.create_example(dto, session)
    return CreateResponseSchema(example_id=example_id)


@router.get("/", response_model=list[ExampleSchema])
async def list_examples(
    session: AsyncSession = Depends(SessionManager.session_factory),
) -> list[ExampleSchema]:
    examples = await ExampleService.list_examples(session)
    return [example.to_schema(ExampleSchema) for example in examples]


@router.get("/{example_id}", response_model=ExampleSchema)
async def get_example(
    example_id: UUID,
    session: AsyncSession = Depends(SessionManager.session_factory),
) -> ExampleSchema:
    example = await ExampleService.get_example(str(example_id), session)
    return example.to_schema(ExampleSchema)


@router.patch("/{example_id}", response_model=ExampleSchema)
async def update_example(
    example_id: UUID,
    data: UpdateSchema,
    session: AsyncSession = Depends(SessionManager.session_factory),
) -> ExampleSchema:
    dto = request_dto.UpdateRequestDTO.from_schema(data)
    example = await ExampleService.update_example(str(example_id), dto, session)
    return example.to_schema(ExampleSchema)


@router.delete("/{example_id}", status_code=204)
async def delete_example(
    example_id: UUID,
    session: AsyncSession = Depends(SessionManager.session_factory),
) -> None:
    await ExampleService.delete_example(str(example_id), session)
