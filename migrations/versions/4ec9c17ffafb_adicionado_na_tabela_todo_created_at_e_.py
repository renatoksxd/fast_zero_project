"""Adicionado na tabela todo created_at e updated_at

Revision ID: 4ec9c17ffafb
Revises: e0b5e393504d
Create Date: 2025-09-05 11:24:20.123368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ec9c17ffafb'
down_revision: Union[str, Sequence[str], None] = 'e0b5e393504d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('todos', schema=None) as batch_op:

        batch_op.add_column(
            sa.Column(
                'created_at',
                sa.DateTime(),
                server_default=sa.text('(CURRENT_TIMESTAMP)'),
                nullable=False,
            )
        )
        batch_op.add_column(
            sa.Column(
                'updated_at',
                sa.DateTime(),
                server_default=sa.text('(CURRENT_TIMESTAMP)'),
                nullable=False,
            )
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.drop_column('created_at')
        batch_op.drop_column('updated_at')
