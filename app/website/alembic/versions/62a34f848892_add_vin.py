"""add vin

Revision ID: 62a34f848892
Revises: 4dfb312e6d73
Create Date: 2024-07-08 05:09:28.229482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62a34f848892'
down_revision = '2bcd646b54f2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('adv', sa.Column('vin', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('adv', 'vin')
    # ### end Alembic commands ###
