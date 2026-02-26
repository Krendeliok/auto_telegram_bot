"""Change telegram_id type

Revision ID: f45bd5b387f6
Revises: d53dba9de670
Create Date: 2026-02-26 18:21:27.167574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f45bd5b387f6'
down_revision = 'd53dba9de670'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "client",
        "telegram_id",
        existing_type=sa.Integer(),
        type_=sa.String(),
        postgresql_using="telegram_id::text",
    )

def downgrade():
    op.alter_column(
        "client",
        "telegram_id",
        existing_type=sa.String(),
        type_=sa.Integer(),
        postgresql_using="telegram_id::integer",
    )
