"""make_email_required

Revision ID: 70f30a12c96c
Revises: 4199a5b4252a
Create Date: 2026-02-19 13:33:55.571112

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '70f30a12c96c'
down_revision: str | Sequence[str] | None = '4199a5b4252a'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Ensure email is required (idempotent operation)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
