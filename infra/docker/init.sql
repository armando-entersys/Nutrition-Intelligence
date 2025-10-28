-- Database initialization script
-- This script creates the initial database structure for Nutrition Intelligence

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create schemas
CREATE SCHEMA IF NOT EXISTS users;
CREATE SCHEMA IF NOT EXISTS nutrition;
CREATE SCHEMA IF NOT EXISTS consultations;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE nutrition_intelligence TO postgres;
