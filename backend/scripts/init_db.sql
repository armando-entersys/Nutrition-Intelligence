-- ============================================================================
-- Nutrition Intelligence - PostgreSQL Initialization Script
-- ============================================================================

-- This script is automatically executed when the PostgreSQL container starts
-- for the first time. It sets up the database with proper extensions and
-- initial configuration.

-- ============================================================================
-- CREATE EXTENSIONS
-- ============================================================================

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable pgcrypto for password hashing
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Enable full text search in Spanish
CREATE EXTENSION IF NOT EXISTS "unaccent";

-- ============================================================================
-- CONFIGURE TEXT SEARCH
-- ============================================================================

-- Create Spanish text search configuration
CREATE TEXT SEARCH CONFIGURATION spanish_unaccent (COPY = spanish);
ALTER TEXT SEARCH CONFIGURATION spanish_unaccent
  ALTER MAPPING FOR hword, hword_part, word WITH unaccent, spanish_stem;

-- ============================================================================
-- GRANT PERMISSIONS
-- ============================================================================

-- Grant all privileges to nutrition_user on the database
GRANT ALL PRIVILEGES ON DATABASE nutrition_intelligence TO nutrition_user;

-- Grant usage on schema
GRANT ALL ON SCHEMA public TO nutrition_user;

-- ============================================================================
-- SET DEFAULT PRIVILEGES
-- ============================================================================

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT ALL ON TABLES TO nutrition_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT ALL ON SEQUENCES TO nutrition_user;

-- ============================================================================
-- INITIAL CONFIGURATION
-- ============================================================================

-- Set timezone to Mexico City
SET TIMEZONE='America/Mexico_City';

-- Log completion
\echo '✅ Database nutrition_intelligence initialized successfully'
\echo '📊 Extensions created: uuid-ossp, pgcrypto, unaccent'
\echo '🔐 Permissions granted to nutrition_user'
\echo '🇲🇽 Timezone set to America/Mexico_City'
