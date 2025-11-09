-- Migration: Create notifications table and enums
-- Date: 2025-11-08
-- Description: Creates complete notification system with types, priorities, and statuses

-- ============================================================================
-- CREATE ENUM TYPES
-- ============================================================================

-- Create notification_type enum
CREATE TYPE notification_type AS ENUM (
    'info',
    'success',
    'warning',
    'error',
    'appointment',
    'meal_plan',
    'progress',
    'system'
);

-- Create notification_priority enum
CREATE TYPE notification_priority AS ENUM (
    'low',
    'medium',
    'high',
    'urgent'
);

-- Create notification_status enum
CREATE TYPE notification_status AS ENUM (
    'unread',
    'read',
    'archived'
);

-- ============================================================================
-- CREATE NOTIFICATIONS TABLE
-- ============================================================================

CREATE TABLE notifications (
    -- Primary key
    id SERIAL PRIMARY KEY,

    -- User relationship
    user_id INTEGER NOT NULL REFERENCES auth_users(id) ON DELETE CASCADE,

    -- Notification content
    title VARCHAR(255) NOT NULL,
    message VARCHAR(1000) NOT NULL,
    icon VARCHAR(50),

    -- Classification
    type notification_type NOT NULL DEFAULT 'info',
    priority notification_priority NOT NULL DEFAULT 'medium',
    status notification_status NOT NULL DEFAULT 'unread',

    -- Action/Navigation (JSON fields)
    action JSONB,
    action_url VARCHAR(500),
    action_label VARCHAR(100),

    -- Metadata (renamed to meta_data to avoid SQLAlchemy reserved keyword)
    meta_data JSONB,

    -- Related entities
    related_entity_type VARCHAR(50),
    related_entity_id INTEGER,

    -- Scheduling
    scheduled_for TIMESTAMP,
    expires_at TIMESTAMP,

    -- Read tracking
    read_at TIMESTAMP,
    archived_at TIMESTAMP,

    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP
);

-- ============================================================================
-- CREATE INDEXES
-- ============================================================================

-- Index for user lookups (most common query)
CREATE INDEX idx_notifications_user_id ON notifications(user_id);

-- Index for unread notifications query
CREATE INDEX idx_notifications_user_status ON notifications(user_id, status);

-- Index for filtering by type
CREATE INDEX idx_notifications_type ON notifications(type);

-- Index for filtering by priority
CREATE INDEX idx_notifications_priority ON notifications(priority);

-- Index for ordering by creation date
CREATE INDEX idx_notifications_created_at ON notifications(created_at DESC);

-- Index for scheduled notifications
CREATE INDEX idx_notifications_scheduled ON notifications(scheduled_for) WHERE scheduled_for IS NOT NULL;

-- Index for expired notifications
CREATE INDEX idx_notifications_expires ON notifications(expires_at) WHERE expires_at IS NOT NULL;

-- Composite index for common query pattern (user + status + created_at)
CREATE INDEX idx_notifications_user_status_created ON notifications(user_id, status, created_at DESC);

-- ============================================================================
-- ADD COMMENTS FOR DOCUMENTATION
-- ============================================================================

COMMENT ON TABLE notifications IS 'Sistema de notificaciones para usuarios';

COMMENT ON COLUMN notifications.id IS 'ID único de la notificación';
COMMENT ON COLUMN notifications.user_id IS 'ID del usuario que recibe la notificación';
COMMENT ON COLUMN notifications.title IS 'Título de la notificación';
COMMENT ON COLUMN notifications.message IS 'Mensaje detallado de la notificación';
COMMENT ON COLUMN notifications.icon IS 'Emoji o identificador de icono';
COMMENT ON COLUMN notifications.type IS 'Tipo de notificación (info, success, warning, error, appointment, meal_plan, progress, system)';
COMMENT ON COLUMN notifications.priority IS 'Prioridad de la notificación (low, medium, high, urgent)';
COMMENT ON COLUMN notifications.status IS 'Estado de la notificación (unread, read, archived)';
COMMENT ON COLUMN notifications.action IS 'Payload JSON de la acción (ej: {type: "navigate", target: "appointments"})';
COMMENT ON COLUMN notifications.action_url IS 'URL a la que navegar cuando se hace clic';
COMMENT ON COLUMN notifications.action_label IS 'Etiqueta del botón de acción';
COMMENT ON COLUMN notifications.meta_data IS 'Metadatos adicionales en formato JSON';
COMMENT ON COLUMN notifications.related_entity_type IS 'Tipo de entidad relacionada (patient, meal_plan, appointment, etc.)';
COMMENT ON COLUMN notifications.related_entity_id IS 'ID de la entidad relacionada';
COMMENT ON COLUMN notifications.scheduled_for IS 'Fecha/hora para mostrar la notificación (notificaciones programadas)';
COMMENT ON COLUMN notifications.expires_at IS 'Fecha/hora de expiración para auto-archivar';
COMMENT ON COLUMN notifications.read_at IS 'Fecha/hora en que se marcó como leída';
COMMENT ON COLUMN notifications.archived_at IS 'Fecha/hora en que se archivó';
COMMENT ON COLUMN notifications.created_at IS 'Fecha/hora de creación';
COMMENT ON COLUMN notifications.updated_at IS 'Fecha/hora de última actualización';

-- ============================================================================
-- GRANT PERMISSIONS (if needed)
-- ============================================================================

-- Grant permissions to the application user (adjust user name as needed)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON notifications TO nutrition_user;
-- GRANT USAGE, SELECT ON SEQUENCE notifications_id_seq TO nutrition_user;
