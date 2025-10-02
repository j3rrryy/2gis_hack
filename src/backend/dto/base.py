from dataclasses import asdict, dataclass, replace
from typing import Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T", bound="BaseDTO")
Schema = TypeVar("Schema", bound=BaseModel)
Model = TypeVar("Model", bound=DeclarativeBase)


@dataclass(slots=True, frozen=True)
class BaseDTO:
    def replace(self: T, **kwargs) -> T:
        return replace(self, **kwargs)


@dataclass(slots=True, frozen=True)
class FromSchemaMixin(BaseDTO):
    @classmethod
    def from_schema(cls: Type[T], schema: BaseModel) -> T:
        return cls(**{f: getattr(schema, f) for f in cls.__dataclass_fields__.keys()})


@dataclass(slots=True, frozen=True)
class ToSchemaMixin(BaseDTO):
    def to_schema(self, schema: type[Schema]) -> Schema:
        return schema(**{f: getattr(self, f) for f in schema.model_fields.keys()})


@dataclass(slots=True, frozen=True)
class FromModelMixin(BaseDTO):
    @classmethod
    def from_model(cls: Type[T], model: DeclarativeBase) -> T:
        return cls(**{f: getattr(model, f) for f in cls.__dataclass_fields__.keys()})


@dataclass(slots=True, frozen=True)
class ToModelMixin(BaseDTO):
    def to_model(self, model: type[Model]) -> Model:
        return model(**asdict(self))
