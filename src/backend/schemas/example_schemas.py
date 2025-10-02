from pydantic import BaseModel, Field


class CreateRequestSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=88)


class CreateResponseSchema(BaseModel):
    example_id: str


class ExampleSchema(BaseModel):
    example_id: str
    name: str


class UpdateSchema(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=88)
