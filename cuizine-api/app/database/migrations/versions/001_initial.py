"""initial

Revision ID: 001
Revises: 
Create Date: 2024-11-17 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create tags table first
    op.create_table(
        'tags',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create recipes table
    op.create_table(
        'recipes',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('difficulty_level', sa.String(), nullable=True),
        sa.Column('prep_time', sa.Integer(), nullable=True),
        sa.Column('cook_time', sa.Integer(), nullable=True),
        sa.Column('total_time', sa.Integer(), nullable=True),
        sa.Column('servings', sa.Integer(), nullable=True),
        sa.Column('cuisine_type', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('meal_type', sa.String(), nullable=True),
        sa.Column('cooking_style', sa.String(), nullable=True),
        sa.Column('preparation_method', sa.String(), nullable=True),
        sa.Column('is_spicy', sa.Boolean(), default=False),
        sa.Column('ingredients', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('instructions', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('equipment_needed', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('nutritional_info', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('dietary_info', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('recipe_tips', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('storage_instructions', sa.String(), nullable=True),
        sa.Column('scaling_notes', sa.String(), nullable=True),
        sa.Column('leftover_ideas', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('source_type', sa.String(), nullable=True),
        sa.Column('generated_from', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('creator_user_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.Column('view_count', sa.Integer(), default=0),
        sa.Column('like_count', sa.Integer(), default=0),
        sa.Column('save_count', sa.Integer(), default=0),
        sa.PrimaryKeyConstraint('id')
    )

    # Create other tables and relationships
    op.create_table(
        'recipe_tags',
        sa.Column('recipe_id', sa.String(), nullable=False),
        sa.Column('tag_id', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id']),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id']),
        sa.PrimaryKeyConstraint('recipe_id', 'tag_id')
    )

    # Add indexes
    op.create_index('idx_recipes_creator', 'recipes', ['creator_user_id'])
    op.create_index('idx_recipes_cuisine', 'recipes', ['cuisine_type'])
    op.create_index('idx_recipes_meal_type', 'recipes', ['meal_type'])

def downgrade() -> None:
    op.drop_index('idx_recipes_meal_type')
    op.drop_index('idx_recipes_cuisine')
    op.drop_index('idx_recipes_creator')
    op.drop_table('recipe_tags')
    op.drop_table('recipes')
    op.drop_table('tags')