-- Initialize database tables for Nutrition Intelligence
-- This script creates all necessary tables and indexes

-- Drop existing tables if they exist
DROP TABLE IF EXISTS password_reset_tokens CASCADE;
DROP TABLE IF EXISTS auth_users CASCADE;

-- Create auth_users table
CREATE TABLE auth_users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    account_status VARCHAR(20) DEFAULT 'pending_verification',
    is_email_verified BOOLEAN DEFAULT FALSE,
    is_phone_verified BOOLEAN DEFAULT FALSE,
    primary_role VARCHAR(20) NOT NULL,
    secondary_roles JSONB DEFAULT '[]'::jsonb,
    last_login TIMESTAMP,
    login_count INTEGER DEFAULT 0,
    failed_login_attempts INTEGER DEFAULT 0,
    last_failed_login TIMESTAMP,
    password_changed_at TIMESTAMP,
    profile_completed BOOLEAN DEFAULT FALSE,
    preferences JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    nutritionist_id INTEGER REFERENCES auth_users(id)
);

-- Create indexes for auth_users
CREATE INDEX idx_auth_users_email ON auth_users(email);
CREATE INDEX idx_auth_users_username ON auth_users(username);
CREATE INDEX idx_auth_users_primary_role ON auth_users(primary_role);
CREATE INDEX idx_auth_users_nutritionist_id ON auth_users(nutritionist_id);

-- Create password_reset_tokens table
CREATE TABLE password_reset_tokens (
    id SERIAL PRIMARY KEY,
    token VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES auth_users(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    expires_at TIMESTAMP NOT NULL,
    used_at TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for password_reset_tokens
CREATE INDEX idx_password_reset_tokens_token ON password_reset_tokens(token);
CREATE INDEX idx_password_reset_tokens_user_id ON password_reset_tokens(user_id);
CREATE INDEX idx_password_reset_tokens_email ON password_reset_tokens(email);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO nutrition_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO nutrition_user;

SELECT 'Tables created successfully' as status;
