"""initial

Revision ID: ac1b583267eb
Revises:
Create Date: 2025-10-02 09:23:48.521551

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ac1b583267eb"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "examples",
        sa.Column("example_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("example_id"),
        sa.UniqueConstraint("name"),
    )


def downgrade() -> None:
    op.drop_table("examples")
