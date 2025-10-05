from datetime import datetime
from uuid import uuid4

import sqlalchemy as sa
from geoalchemy2 import Geography, WKBElement
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from enums import CalculationStatus

Base = declarative_base()


class Calculation(Base):
    __tablename__ = "calculations"

    calculation_id: Mapped[str] = mapped_column(
        UUID(False), primary_key=True, default=uuid4
    )
    coordinate: Mapped[WKBElement] = mapped_column(
        Geography("POINT", srid=4326), nullable=False
    )
    result: Mapped[int] = mapped_column(sa.Integer, nullable=True)
    status: Mapped[str] = mapped_column(
        sa.String(20), nullable=False, server_default=CalculationStatus.PENDING.value
    )
    scheduled_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP(True), nullable=False, server_default=sa.func.now()
    )
    calculated_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP(True), nullable=True)

    def __str__(self) -> str:
        return f"<Calculation: {self.calculation_id}>"
