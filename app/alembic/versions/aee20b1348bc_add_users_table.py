"""add users table

Revision ID: aee20b1348bc
Revises: a734660a917c
Create Date: 2025-12-22 15:30:21.168201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aee20b1348bc'
down_revision: Union[str, Sequence[str], None] = 'a734660a917c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
                    sa.Column('id', sa.Integer(),nullable=False),
                    sa.Column('email', sa.String(255),nullable=False),
                    sa.Column('password', sa.String(100),nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users')
    pass
