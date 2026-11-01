"""enable postgis

Revision ID: dff1ac55d5da
Revises: None
Create Date: 2026-11-01
"""

from collections.abc import Sequence

from alembic import op

revision: str = "dff1ac55d5da"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS postgis")
