"""Add lessons/course created_at index (no-op placeholder)

Revision ID: d1e2f3g4h5i6
Revises: c370a8758236
Create Date: 2025-11-06 09:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd1e2f3g4h5i6'
down_revision = 'c370a8758236'
branch_labels = None
depends_on = None


def upgrade():
	# placeholder migration: create index if not exists (some DBs may ignore)
	try:
		op.create_index(op.f('ix_lessons_created_at'), 'lessons', ['created_at'], unique=False)
	except Exception:
		pass


def downgrade():
	try:
		op.drop_index(op.f('ix_lessons_created_at'), table_name='lessons')
	except Exception:
		pass
