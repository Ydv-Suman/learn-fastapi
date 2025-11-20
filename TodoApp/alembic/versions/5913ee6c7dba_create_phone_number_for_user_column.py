"""Create Phone number for user column

Revision ID: 5913ee6c7dba
Revises: 
Create Date: 2025-11-20 13:08:16.853490

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # pyright: ignore[reportUnusedImport, reportMissingImports]


# revision identifiers, used by Alembic.
revision: str = '5913ee6c7dba'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String, nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
