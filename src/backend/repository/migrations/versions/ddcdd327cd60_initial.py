"""initial

Revision ID: ddcdd327cd60
Revises:
Create Date: 2025-10-04 20:55:35.544789

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from geoalchemy2 import Geography

# revision identifiers, used by Alembic.
revision: str = "ddcdd327cd60"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_geospatial_table(  # pyright: ignore[reportAttributeAccessIssue]
        "calculations",
        sa.Column("calculation_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column(
            "coordinate",
            Geography(
                geometry_type="POINT",
                srid=4326,
                dimension=2,
                spatial_index=False,
                from_text="ST_GeogFromText",
                name="geography",
                nullable=False,
            ),
            nullable=False,
        ),
        sa.Column("result", sa.Float(), nullable=False),
        sa.Column(
            "is_ready", sa.Boolean(), server_default=sa.text("false"), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("calculated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("calculation_id"),
    )
    op.create_geospatial_index(  # pyright: ignore[reportAttributeAccessIssue]
        "idx_calculations_coordinate",
        "calculations",
        ["coordinate"],
        unique=False,
        postgresql_using="gist",
        postgresql_ops={},
    )


def downgrade() -> None:
    op.drop_geospatial_index(  # pyright: ignore[reportAttributeAccessIssue]
        "idx_calculations_coordinate",
        table_name="calculations",
        postgresql_using="gist",
        column_name="coordinate",
    )
    op.drop_geospatial_table("calculations")  # pyright: ignore[reportAttributeAccessIssue]
