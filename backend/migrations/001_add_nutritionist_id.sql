-- Migration: Add nutritionist_id to auth_users table
-- Date: 2025-11-04
-- Description: Adds patient-nutritionist relationship to support linking patients to nutritionists

-- Add nutritionist_id column to auth_users table
ALTER TABLE auth_users
ADD COLUMN nutritionist_id INTEGER NULL
REFERENCES auth_users(id);

-- Add index for better query performance on nutritionist lookups
CREATE INDEX idx_auth_users_nutritionist_id ON auth_users(nutritionist_id);

-- Add comment to column for documentation
COMMENT ON COLUMN auth_users.nutritionist_id IS 'ID del nutriólogo asignado (solo para pacientes)';
