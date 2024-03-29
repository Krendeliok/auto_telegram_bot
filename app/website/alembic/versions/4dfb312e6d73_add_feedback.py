"""add Feedback

Revision ID: 4dfb312e6d73
Revises: acf50b6fde26
Create Date: 2023-11-12 18:22:20.029788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4dfb312e6d73'
down_revision = 'acf50b6fde26'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feedback',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('advertisement_id', sa.Integer(), nullable=True),
    sa.Column('verified', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.ForeignKeyConstraint(['advertisement_id'], ['adv.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feedback')
    # ### end Alembic commands ###
