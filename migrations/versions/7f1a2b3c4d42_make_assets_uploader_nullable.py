"""make assets.uploader_id nullable

Revision ID: 7f1a2b3c4d42
Revises: c370a8758236
Create Date: 2025-10-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7f1a2b3c4d42'
down_revision = 'c370a8758236'
branch_labels = None
depends_on = None


def upgrade():
    # make uploader_id nullable so anonymous uploads can be recorded
    with op.batch_alter_table('assets', schema=None) as batch_op:
        batch_op.alter_column('uploader_id', existing_type=sa.Integer(), nullable=True)


def downgrade():
    # revert to not nullable
    with op.batch_alter_table('assets', schema=None) as batch_op:
        batch_op.alter_column('uploader_id', existing_type=sa.Integer(), nullable=False)
