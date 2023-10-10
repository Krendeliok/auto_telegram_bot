"""Filters

Revision ID: 23cce1d52a11
Revises: 87c43dde5cee
Create Date: 2022-11-25 14:52:40.849467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23cce1d52a11'
down_revision = '87c43dde5cee'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('filter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('min_price', sa.Integer(), nullable=False),
    sa.Column('max_price', sa.Integer(), nullable=False),
    sa.Column('min_year', sa.Integer(), nullable=False),
    sa.Column('max_year', sa.Integer(), nullable=False),
    sa.Column('min_engine_volume', sa.Float(), nullable=False),
    sa.Column('max_engine_volume', sa.Float(), nullable=False),
    sa.Column('min_range', sa.Integer(), nullable=False),
    sa.Column('max_range', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['client.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('engine_filter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filter_id', sa.Integer(), nullable=True),
    sa.Column('engine_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['engine_id'], ['engine.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['filter_id'], ['filter.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gearbox_filter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filter_id', sa.Integer(), nullable=True),
    sa.Column('gearbox_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['filter_id'], ['filter.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['gearbox_id'], ['gearbox.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('model_filter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filter_id', sa.Integer(), nullable=True),
    sa.Column('model_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['filter_id'], ['filter.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['model_id'], ['model.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('producer_filter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filter_id', sa.Integer(), nullable=True),
    sa.Column('producer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['filter_id'], ['filter.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['producer_id'], ['producer.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('region_filter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filter_id', sa.Integer(), nullable=True),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['filter_id'], ['filter.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['region_id'], ['country.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('region_filter')
    op.drop_table('producer_filter')
    op.drop_table('model_filter')
    op.drop_table('gearbox_filter')
    op.drop_table('engine_filter')
    op.drop_table('filter')
    # ### end Alembic commands ###