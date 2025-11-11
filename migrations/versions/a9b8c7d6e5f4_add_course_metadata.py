"""Add course metadata and thumbnail FK

Revision ID: a9b8c7d6e5f4
Revises: merge_8a2_a1b2
Create Date: 2025-11-06 09:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a9b8c7d6e5f4'
down_revision = 'merge_8a2_a1b2'
branch_labels = None
depends_on = None


def upgrade():
    # create enum type for difficulty (if DB supports ENUM)
    try:
        course_diff = sa.Enum('beginner', 'intermediate', 'advanced', name='course_difficulty')
        course_diff.create(op.get_bind(), checkfirst=True)
    except Exception:
        # some backends (sqlite) ignore enum creation
        pass

    # add new columns to courses table
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('thumbnail_url', sa.String(length=1024), nullable=True))
        batch_op.add_column(sa.Column('thumbnail_asset_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('category', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('class_name', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('price', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('published', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('featured', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('duration_weeks', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('weekly_hours', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('difficulty', sa.Enum('beginner','intermediate','advanced', name='course_difficulty'), nullable=True))
        batch_op.add_column(sa.Column('stream', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('tags', sa.Text(), nullable=True))

    # create index on some new fields
    with op.batch_alter_table('courses', schema=None) as batch_op:
        try:
            batch_op.create_index(batch_op.f('ix_courses_category'), ['category'], unique=False)
            batch_op.create_index(batch_op.f('ix_courses_class_name'), ['class_name'], unique=False)
            batch_op.create_index(batch_op.f('ix_courses_difficulty'), ['difficulty'], unique=False)
        except Exception:
            pass

    # create foreign key to assets for thumbnail_asset_id
    try:
        op.create_foreign_key('fk_courses_thumbnail_asset', 'courses', 'assets', ['thumbnail_asset_id'], ['id'])
    except Exception:
        # some backends may not support FK alterations in simple manner
        pass


def downgrade():
    # drop FK
    try:
        op.drop_constraint('fk_courses_thumbnail_asset', 'courses', type_='foreignkey')
    except Exception:
        pass

    # drop indexes and columns
    with op.batch_alter_table('courses', schema=None) as batch_op:
        try:
            batch_op.drop_index(batch_op.f('ix_courses_difficulty'))
        except Exception:
            pass
        try:
            batch_op.drop_index(batch_op.f('ix_courses_class_name'))
        except Exception:
            pass
        try:
            batch_op.drop_index(batch_op.f('ix_courses_category'))
        except Exception:
            pass

        batch_op.drop_column('tags')
        batch_op.drop_column('stream')
        batch_op.drop_column('difficulty')
        batch_op.drop_column('weekly_hours')
        batch_op.drop_column('duration_weeks')
        batch_op.drop_column('featured')
        batch_op.drop_column('published')
        batch_op.drop_column('price')
        batch_op.drop_column('class_name')
        batch_op.drop_column('category')
        batch_op.drop_column('thumbnail_asset_id')
        batch_op.drop_column('thumbnail_url')

    # drop enum type if exists
    try:
        course_diff = sa.Enum(name='course_difficulty')
        course_diff.drop(op.get_bind(), checkfirst=True)
    except Exception:
        pass
