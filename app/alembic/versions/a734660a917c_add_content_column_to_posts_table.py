"""add content column to posts table

Revision ID: a734660a917c
Revises: 1c1a073275c4
Create Date: 2025-12-22 15:20:35.310083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a734660a917c'
down_revision: Union[str, Sequence[str], None] = '1c1a073275c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(255),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
