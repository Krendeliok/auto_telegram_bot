"""add publish date

Revision ID: 87c43dde5cee
Revises: e73370c3ed36
Create Date: 2022-11-25 11:54:14.679320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87c43dde5cee'
down_revision = 'e73370c3ed36'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('adv', sa.Column('last_published_date', sa.Date(), nullable=True))
    op.add_column('adv', sa.Column('next_published_date', sa.Date(), nullable=True))
    op.alter_column('adv', 'gearbox_type_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('adv', 'based_country_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('adv', 'based_country_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('adv', 'gearbox_type_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('adv', 'next_published_date')
    op.drop_column('adv', 'last_published_date')
    # ### end Alembic commands ###
