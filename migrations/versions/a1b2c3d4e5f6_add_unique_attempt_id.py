"""add unique constraint on progress.attempt_id

Revision ID: a1b2c3d4e5f6
Revises: 7f1a2b3c4d42
Create Date: 2025-10-28 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '7f1a2b3c4d42'
branch_labels = None
depends_on = None


def upgrade():
    # Create a unique index on attempt_id to prevent duplicate attempts when provided
    # MySQL allows multiple NULLs for unique indexes so anonymous submissions won't be blocked.
    op.create_index('uq_progress_attempt_id', 'progress', ['attempt_id'], unique=True)


def downgrade():
    op.drop_index('uq_progress_attempt_id', table_name='progress')
