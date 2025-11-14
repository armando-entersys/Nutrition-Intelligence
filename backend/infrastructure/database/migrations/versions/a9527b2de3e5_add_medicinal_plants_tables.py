"""Add medicinal plants tables

Revision ID: a9527b2de3e5
Revises: 2155b0e78aa7
Create Date: 2025-11-13 20:00:32.928363

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'a9527b2de3e5'
down_revision = '2155b0e78aa7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create medicinal_plants table
    op.create_table(
        'medicinal_plants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('scientific_name', sa.String(length=300), nullable=False),
        sa.Column('botanical_family', sa.String(length=200), nullable=True),
        sa.Column('popular_names', sa.JSON(), nullable=False),
        sa.Column('indigenous_names', sa.JSON(), nullable=True),
        sa.Column('states_found', sa.JSON(), nullable=False),
        sa.Column('origin_region', sa.String(length=200), nullable=True),
        sa.Column('growing_season', sa.JSON(), nullable=True),
        sa.Column('primary_category', sa.String(length=50), nullable=False),
        sa.Column('secondary_categories', sa.JSON(), nullable=True),
        sa.Column('traditional_uses', sa.JSON(), nullable=False),
        sa.Column('indigenous_uses', sa.JSON(), nullable=True),
        sa.Column('preparation_methods', sa.JSON(), nullable=False),
        sa.Column('active_compounds', sa.JSON(), nullable=True),
        sa.Column('pharmacological_actions', sa.JSON(), nullable=True),
        sa.Column('evidence_level', sa.String(length=50), nullable=False),
        sa.Column('clinical_studies_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('proven_effects', sa.JSON(), nullable=True),
        sa.Column('safety_level', sa.String(length=50), nullable=False),
        sa.Column('precautions', sa.JSON(), nullable=True),
        sa.Column('contraindications', sa.JSON(), nullable=True),
        sa.Column('adverse_effects', sa.JSON(), nullable=True),
        sa.Column('drug_interactions', sa.JSON(), nullable=True),
        sa.Column('safe_in_pregnancy', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('safe_in_lactation', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('safe_for_children', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('minimum_age_years', sa.Integer(), nullable=True),
        sa.Column('availability_level', sa.String(length=20), nullable=False, server_default='MEDIUM'),
        sa.Column('where_to_find', sa.JSON(), nullable=False),
        sa.Column('approximate_price_range', sa.String(length=100), nullable=True),
        sa.Column('plant_description', sa.Text(), nullable=True),
        sa.Column('identification_features', sa.JSON(), nullable=True),
        sa.Column('main_image_url', sa.String(length=500), nullable=True),
        sa.Column('additional_images', sa.JSON(), nullable=True),
        sa.Column('video_url', sa.String(length=500), nullable=True),
        sa.Column('source', sa.String(length=200), nullable=False, server_default='UNAM'),
        sa.Column('source_urls', sa.JSON(), nullable=True),
        sa.Column('validated_by_expert', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('last_validated_at', sa.DateTime(), nullable=True),
        sa.Column('historical_notes', sa.Text(), nullable=True),
        sa.Column('ritual_ceremonial_use', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('featured', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('view_count', sa.Integer(), nullable=False, server_default='0'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_medicinal_plants_scientific_name'), 'medicinal_plants', ['scientific_name'], unique=True)

    # Create user_plant_logs table
    op.create_table(
        'user_plant_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('plant_id', sa.Integer(), nullable=False),
        sa.Column('date_started', sa.DateTime(), nullable=False),
        sa.Column('date_ended', sa.DateTime(), nullable=True),
        sa.Column('still_using', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('preparation_type', sa.String(length=50), nullable=False),
        sa.Column('dosage_used', sa.String(length=300), nullable=False),
        sa.Column('frequency', sa.String(length=200), nullable=False),
        sa.Column('reason_for_use', sa.String(length=500), nullable=False),
        sa.Column('observed_effects', sa.Text(), nullable=True),
        sa.Column('effectiveness_rating', sa.Integer(), nullable=True),
        sa.Column('adverse_effects_experienced', sa.Text(), nullable=True),
        sa.Column('discontinued_reason', sa.String(length=500), nullable=True),
        sa.Column('recommended_by_nutritionist', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('nutritionist_id', sa.Integer(), nullable=True),
        sa.Column('taking_medications', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('medications_list', sa.JSON(), nullable=True),
        sa.Column('doctor_consulted', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['plant_id'], ['medicinal_plants.id'], ),
        sa.ForeignKeyConstraint(['nutritionist_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_plant_logs_user_id'), 'user_plant_logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_plant_logs_plant_id'), 'user_plant_logs', ['plant_id'], unique=False)

    # Create plant_health_conditions table
    op.create_table(
        'plant_health_conditions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plant_id', sa.Integer(), nullable=False),
        sa.Column('condition_name', sa.String(length=200), nullable=False),
        sa.Column('condition_category', sa.String(length=100), nullable=False),
        sa.Column('effectiveness_level', sa.String(length=50), nullable=False),
        sa.Column('traditional_use', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('scientific_evidence', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('mechanism_of_action', sa.Text(), nullable=True),
        sa.Column('recommended_dosage', sa.String(length=500), nullable=True),
        sa.Column('treatment_duration', sa.String(length=200), nullable=True),
        sa.Column('studies_references', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['plant_id'], ['medicinal_plants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plant_health_conditions_plant_id'), 'plant_health_conditions', ['plant_id'], unique=False)
    op.create_index(op.f('ix_plant_health_conditions_condition_name'), 'plant_health_conditions', ['condition_name'], unique=False)

    # Create herbal_shops table
    op.create_table(
        'herbal_shops',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=300), nullable=False),
        sa.Column('shop_type', sa.String(length=100), nullable=False),
        sa.Column('address', sa.String(length=500), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=False),
        sa.Column('state', sa.String(length=100), nullable=False),
        sa.Column('postal_code', sa.String(length=10), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('email', sa.String(length=200), nullable=True),
        sa.Column('website', sa.String(length=300), nullable=True),
        sa.Column('hours_of_operation', sa.JSON(), nullable=True),
        sa.Column('average_rating', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('total_reviews', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('verified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('verified_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_herbal_shops_city'), 'herbal_shops', ['city'], unique=False)
    op.create_index(op.f('ix_herbal_shops_state'), 'herbal_shops', ['state'], unique=False)

    # Create plant_recommendations table
    op.create_table(
        'plant_recommendations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('recommended_plants', sa.JSON(), nullable=False),
        sa.Column('based_on_health_profile', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('health_conditions', sa.JSON(), nullable=True),
        sa.Column('symptoms', sa.JSON(), nullable=True),
        sa.Column('ai_reasoning', sa.Text(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('user_viewed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('user_accepted', sa.Boolean(), nullable=True),
        sa.Column('user_feedback', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plant_recommendations_user_id'), 'plant_recommendations', ['user_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_plant_recommendations_user_id'), table_name='plant_recommendations')
    op.drop_table('plant_recommendations')

    op.drop_index(op.f('ix_herbal_shops_state'), table_name='herbal_shops')
    op.drop_index(op.f('ix_herbal_shops_city'), table_name='herbal_shops')
    op.drop_table('herbal_shops')

    op.drop_index(op.f('ix_plant_health_conditions_condition_name'), table_name='plant_health_conditions')
    op.drop_index(op.f('ix_plant_health_conditions_plant_id'), table_name='plant_health_conditions')
    op.drop_table('plant_health_conditions')

    op.drop_index(op.f('ix_user_plant_logs_plant_id'), table_name='user_plant_logs')
    op.drop_index(op.f('ix_user_plant_logs_user_id'), table_name='user_plant_logs')
    op.drop_table('user_plant_logs')

    op.drop_index(op.f('ix_medicinal_plants_scientific_name'), table_name='medicinal_plants')
    op.drop_table('medicinal_plants')