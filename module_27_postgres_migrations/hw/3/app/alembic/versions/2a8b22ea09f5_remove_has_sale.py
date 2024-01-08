"""Remove has_sale

Revision ID: 2a8b22ea09f5
Revises: 013073baa026
Create Date: 2023-12-27 18:26:42.983298

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a8b22ea09f5'
down_revision: Union[str, None] = '013073baa026'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'has_sale')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('has_sale', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###