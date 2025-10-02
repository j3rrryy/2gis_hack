from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class Example(Base):
    __tablename__ = "examples"

    example_id: Mapped[str] = mapped_column(
        UUID(False), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(sa.String(100), unique=True, nullable=False)

    def __str__(self) -> str:
        return f"<Example: {self.example_id}>"
