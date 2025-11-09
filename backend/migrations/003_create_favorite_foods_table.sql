-- Migration: Create favorite_foods table
-- Date: 2025-11-09
-- Description: Creates table for user favorite foods (many-to-many relationship)

-- ============================================================================
-- CREATE FAVORITE_FOODS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS favorite_foods (
    -- Primary key
    id SERIAL PRIMARY KEY,

    -- Foreign keys
    user_id INTEGER NOT NULL REFERENCES auth_users(id) ON DELETE CASCADE,
    food_id INTEGER NOT NULL REFERENCES foods(id) ON DELETE CASCADE,

    -- Metadata
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    notes VARCHAR(500),  -- Optional user notes about why they like this food

    -- Unique constraint: un usuario solo puede marcar un alimento como favorito una vez
    CONSTRAINT uq_user_food UNIQUE (user_id, food_id)
);

-- ============================================================================
-- CREATE INDEXES
-- ============================================================================

-- Index for user lookups (most common query)
CREATE INDEX idx_favorite_foods_user_id ON favorite_foods(user_id);

-- Index for food lookups
CREATE INDEX idx_favorite_foods_food_id ON favorite_foods(food_id);

-- Composite index for faster joins
CREATE INDEX idx_favorite_foods_user_food ON favorite_foods(user_id, food_id);

-- Index for recent favorites
CREATE INDEX idx_favorite_foods_created_at ON favorite_foods(created_at DESC);

-- ============================================================================
-- ADD COMMENTS FOR DOCUMENTATION
-- ============================================================================

COMMENT ON TABLE favorite_foods IS 'Alimentos favoritos de usuarios (relación many-to-many)';

COMMENT ON COLUMN favorite_foods.id IS 'ID único del registro de favorito';
COMMENT ON COLUMN favorite_foods.user_id IS 'ID del usuario que marcó el alimento como favorito';
COMMENT ON COLUMN favorite_foods.food_id IS 'ID del alimento marcado como favorito';
COMMENT ON COLUMN favorite_foods.created_at IS 'Fecha/hora en que se marcó como favorito';
COMMENT ON COLUMN favorite_foods.notes IS 'Notas opcionales del usuario sobre por qué le gusta este alimento';

-- ============================================================================
-- GRANT PERMISSIONS (if needed)
-- ============================================================================

-- Grant permissions to the application user (adjust user name as needed)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON favorite_foods TO nutrition_user;
-- GRANT USAGE, SELECT ON SEQUENCE favorite_foods_id_seq TO nutrition_user;
