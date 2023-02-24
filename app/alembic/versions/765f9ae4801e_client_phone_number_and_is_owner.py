"""client phone_number and is_owner

Revision ID: 765f9ae4801e
Revises: 068681eb45b1
Create Date: 2022-11-15 09:15:04.730799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '765f9ae4801e'
down_revision = '068681eb45b1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client', sa.Column('phone_number', sa.String(), nullable=False))
    op.add_column('client', sa.Column('is_owner', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('client', 'is_owner')
    op.drop_column('client', 'phone_number')
    # ### end Alembic commands ###
