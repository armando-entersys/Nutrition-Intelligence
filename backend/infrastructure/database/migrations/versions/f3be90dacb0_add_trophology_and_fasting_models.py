"""Add trophology and fasting models

Revision ID: f3be90dacb0
Revises: a9527b2de3e5
Create Date: 2025-11-14 16:56:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'f3be90dacb0'
down_revision = 'a9527b2de3e5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create food_categories table
    op.create_table(
        'food_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('examples', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_food_categories_name'), 'food_categories', ['name'], unique=True)

    # Create food_compatibilities table
    op.create_table(
        'food_compatibilities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('category1_id', sa.Integer(), nullable=False),
        sa.Column('category2_id', sa.Integer(), nullable=False),
        sa.Column('compatible', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('severity', sa.String(length=20), nullable=True),  # HIGH, MEDIUM, LOW
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('page_reference', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['category1_id'], ['food_categories.id'], ),
        sa.ForeignKeyConstraint(['category2_id'], ['food_categories.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_food_compatibilities_category1_id'), 'food_compatibilities', ['category1_id'], unique=False)
    op.create_index(op.f('ix_food_compatibilities_category2_id'), 'food_compatibilities', ['category2_id'], unique=False)

    # Create fasting_windows table
    op.create_table(
        'fasting_windows',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('duration_hours', sa.Integer(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fasting_windows_user_id'), 'fasting_windows', ['user_id'], unique=False)

    # Create fasting_logs table
    op.create_table(
        'fasting_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('window_id', sa.Integer(), nullable=False),
        sa.Column('log_date', sa.Date(), nullable=False),
        sa.Column('first_meal_time', sa.DateTime(), nullable=True),
        sa.Column('last_meal_time', sa.DateTime(), nullable=True),
        sa.Column('fasting_hours', sa.Float(), nullable=True),
        sa.Column('autophagy_hours', sa.Float(), nullable=True),
        sa.Column('adherence', sa.Boolean(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('energy_level', sa.Integer(), nullable=True),
        sa.Column('mental_clarity', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['window_id'], ['fasting_windows.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fasting_logs_user_id'), 'fasting_logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_fasting_logs_window_id'), 'fasting_logs', ['window_id'], unique=False)
    op.create_index(op.f('ix_fasting_logs_log_date'), 'fasting_logs', ['log_date'], unique=False)


def downgrade() -> None:
    # Drop fasting tables
    op.drop_index(op.f('ix_fasting_logs_log_date'), table_name='fasting_logs')
    op.drop_index(op.f('ix_fasting_logs_window_id'), table_name='fasting_logs')
    op.drop_index(op.f('ix_fasting_logs_user_id'), table_name='fasting_logs')
    op.drop_table('fasting_logs')

    op.drop_index(op.f('ix_fasting_windows_user_id'), table_name='fasting_windows')
    op.drop_table('fasting_windows')

    # Drop trophology tables
    op.drop_index(op.f('ix_food_compatibilities_category2_id'), table_name='food_compatibilities')
    op.drop_index(op.f('ix_food_compatibilities_category1_id'), table_name='food_compatibilities')
    op.drop_table('food_compatibilities')

    op.drop_index(op.f('ix_food_categories_name'), table_name='food_categories')
    op.drop_table('food_categories')
