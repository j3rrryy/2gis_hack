from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from di import SessionManager
from dto import request as request_dto
from schemas import CreateRequestSchema, CreateResponseSchema, ReadSchema
from service import ExampleService

router = APIRouter(prefix="/example", tags=["example"])


@router.post("/", status_code=201, response_model=CreateResponseSchema)
async def create(
    data: CreateRequestSchema,
    session: AsyncSession = Depends(SessionManager.session_factory),
) -> CreateResponseSchema:
    dto = request_dto.CreateRequestDTO.from_schema(data)
    example_id = await ExampleService.create(dto, session)
    return CreateResponseSchema(example_id=example_id)


@router.get("/", response_model=list[ReadSchema])
async def read(
    session: AsyncSession = Depends(SessionManager.session_factory),
) -> list[ReadSchema]:
    examples = await ExampleService.read(session)
    return [example.to_schema(ReadSchema) for example in examples]
