"""remove is_superuser column

Revision ID: 4199a5b4252a
Revises: a17917ca66b4
Create Date: 2026-02-19 12:32:17.541556

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4199a5b4252a'
down_revision: str | Sequence[str] | None = 'a17917ca66b4'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('users', 'is_superuser')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), nullable=False,
                                     server_default=sa.false()))
