"""Merge migration to resolve multiple Alembic heads

This is a no-op merge migration whose purpose is to make Alembic's
revision graph linear by declaring both feature revisions as parents.
"""
from alembic import op
import sqlalchemy as sa

revision = 'merge_8a2_a1b2'
down_revision = ('8a2b3c4d5e6f', 'a1b2c3d4e5f6')
branch_labels = None
depends_on = None


def upgrade():
    # no schema changes; this merge revision unifies two heads
    pass


def downgrade():
    # downgrade not supported for merge convenience
    pass
