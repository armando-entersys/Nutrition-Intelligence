-- Database Optimization Script
-- ============================
-- Optimiza índices y rendimiento de PostgreSQL para Nutrition Intelligence

-- Enable pg_trgm extension for similarity searches
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Enable btree_gin for faster multi-column indexes
CREATE EXTENSION IF NOT EXISTS btree_gin;

-- ============================================================================
-- Índices para productos_nom051
-- ============================================================================

-- Índice de búsqueda por texto (nombre y marca)
CREATE INDEX IF NOT EXISTS idx_productos_nom051_nombre_trgm
ON productos_nom051 USING gin (nombre gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_productos_nom051_marca_trgm
ON productos_nom051 USING gin (marca gin_trgm_ops);

-- Índice compuesto para filtros comunes
CREATE INDEX IF NOT EXISTS idx_productos_nom051_global_verified
ON productos_nom051 (is_global, verified)
WHERE is_global = true;

-- Índice para búsquedas por usuario
CREATE INDEX IF NOT EXISTS idx_productos_nom051_user_created
ON productos_nom051 (created_by_user_id, created_at DESC);

-- Índice para productos con excesos (NOM-051)
CREATE INDEX IF NOT EXISTS idx_productos_nom051_excesos
ON productos_nom051 (exceso_calorias, exceso_azucares, exceso_grasas_saturadas, exceso_sodio)
WHERE exceso_calorias = true OR exceso_azucares = true OR exceso_grasas_saturadas = true OR exceso_sodio = true;

-- ============================================================================
-- Índices para alimentos_smae
-- ============================================================================

-- Índice de búsqueda por texto
CREATE INDEX IF NOT EXISTS idx_alimentos_smae_nombre_trgm
ON alimentos_smae USING gin (nombre gin_trgm_ops);

-- Índice para búsquedas por grupo
CREATE INDEX IF NOT EXISTS idx_alimentos_smae_grupo_nombre
ON alimentos_smae (grupo_smae, nombre);

-- Índice para alimentos mexicanos
CREATE INDEX IF NOT EXISTS idx_alimentos_smae_mexicano
ON alimentos_smae (es_mexicano)
WHERE es_mexicano = true;

-- Índice para alimentos verificados
CREATE INDEX IF NOT EXISTS idx_alimentos_smae_verificado
ON alimentos_smae (verificado)
WHERE verificado = true;

-- ============================================================================
-- Índices para auth_users
-- ============================================================================

-- Ya existen, pero vamos a asegurarnos
CREATE INDEX IF NOT EXISTS idx_auth_users_email_lower
ON auth_users (LOWER(email));

CREATE INDEX IF NOT EXISTS idx_auth_users_role_status
ON auth_users (primary_role, account_status);

-- ============================================================================
-- Índices para favorite_foods
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_favorite_foods_user_created
ON favorite_foods (user_id, created_at DESC);

-- ============================================================================
-- Optimización de consultas
-- ============================================================================

-- Actualizar estadísticas para el optimizador
ANALYZE productos_nom051;
ANALYZE alimentos_smae;
ANALYZE auth_users;
ANALYZE favorite_foods;

-- Configurar parámetros de búsqueda de similitud
-- (0.3 = 30% de similitud mínima)
SET pg_trgm.similarity_threshold = 0.3;

-- ============================================================================
-- Vacuum y limpieza
-- ============================================================================

-- Limpiar y optimizar tablas
VACUUM ANALYZE productos_nom051;
VACUUM ANALYZE alimentos_smae;
VACUUM ANALYZE auth_users;

-- ============================================================================
-- Configuraciones de rendimiento
-- ============================================================================

-- Aumentar work_mem para ordenamientos más rápidos (solo para esta sesión)
SET work_mem = '16MB';

-- Configurar shared_buffers para caché (requiere reinicio de PostgreSQL)
-- ALTER SYSTEM SET shared_buffers = '256MB';

-- Configurar effective_cache_size (RAM disponible para caché del OS)
-- ALTER SYSTEM SET effective_cache_size = '1GB';

SELECT
    'Database optimization completed successfully!' as status,
    COUNT(*) FILTER (WHERE schemaname = 'public') as total_indexes
FROM pg_indexes
WHERE schemaname = 'public';

-- Mostrar tamaño de las tablas principales
SELECT
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
    AND tablename IN ('productos_nom051', 'alimentos_smae', 'auth_users', 'favorite_foods')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
