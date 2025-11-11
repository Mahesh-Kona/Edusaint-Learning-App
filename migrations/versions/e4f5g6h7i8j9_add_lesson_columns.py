"""Add lesson columns for admin UI fields

Revision ID: e4f5g6h7i8j9
Revises: d1e2f3g4h5i6
Create Date: 2025-11-07 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e4f5g6h7i8j9'
down_revision = 'd1e2f3g4h5i6'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to lessons table to store admin UI fields directly
    with op.batch_alter_table('lessons', schema=None) as batch_op:
        try:
            batch_op.add_column(sa.Column('description', sa.Text(), nullable=True))
        except Exception:
            pass
        try:
            batch_op.add_column(sa.Column('duration', sa.Integer(), nullable=True))
        except Exception:
            pass
        try:
            batch_op.add_column(sa.Column('level', sa.String(length=50), nullable=True))
        except Exception:
            pass
        try:
            batch_op.add_column(sa.Column('objectives', sa.Text(), nullable=True))
        except Exception:
            pass


def downgrade():
    with op.batch_alter_table('lessons', schema=None) as batch_op:
        try:
            batch_op.drop_column('objectives')
        except Exception:
            pass
        try:
            batch_op.drop_column('level')
        except Exception:
            pass
        try:
            batch_op.drop_column('duration')
        except Exception:
            pass
        try:
            batch_op.drop_column('description')
        except Exception:
            pass
