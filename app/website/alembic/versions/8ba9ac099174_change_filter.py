"""change filter

Revision ID: 8ba9ac099174
Revises: 23cce1d52a11
Create Date: 2022-11-28 13:00:31.761230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ba9ac099174'
down_revision = '23cce1d52a11'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('filter', sa.Column('all_producers', sa.Boolean(), server_default=sa.text('true'), nullable=True))
    op.add_column('filter', sa.Column('all_gearboxes', sa.Boolean(), server_default=sa.text('true'), nullable=True))
    op.add_column('filter', sa.Column('all_regions', sa.Boolean(), server_default=sa.text('true'), nullable=True))
    op.add_column('filter', sa.Column('all_engine_types', sa.Boolean(), server_default=sa.text('true'), nullable=True))
    op.add_column('model_filter', sa.Column('producer_filter_id', sa.Integer(), nullable=True))
    op.drop_constraint('model_filter_filter_id_fkey', 'model_filter', type_='foreignkey')
    op.create_foreign_key(None, 'model_filter', 'producer_filter', ['producer_filter_id'], ['id'], ondelete='CASCADE')
    op.drop_column('model_filter', 'filter_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('model_filter', sa.Column('filter_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'model_filter', type_='foreignkey')
    op.create_foreign_key('model_filter_filter_id_fkey', 'model_filter', 'filter', ['filter_id'], ['id'], ondelete='CASCADE')
    op.drop_column('model_filter', 'producer_filter_id')
    op.drop_column('filter', 'all_engine_types')
    op.drop_column('filter', 'all_regions')
    op.drop_column('filter', 'all_gearboxes')
    op.drop_column('filter', 'all_producers')
    # ### end Alembic commands ###
