-- =====================================================
-- Migration 005: Refactor NOM-051 Scanner for Global Products
-- =====================================================
-- Fecha: 2025-01-09
-- Descripción: Convierte el sistema de scanner en una red neural global
--              con historial de escaneos por usuario y deduplicación
-- =====================================================

-- =====================================================
-- 1. Modificar tabla productos_nom051 para ser global
-- =====================================================

-- Agregar campos para control global y deduplicación
ALTER TABLE productos_nom051
ADD COLUMN IF NOT EXISTS image_hash VARCHAR(64),  -- Hash de la imagen para deduplicación
ADD COLUMN IF NOT EXISTS created_by_user_id INTEGER REFERENCES auth_users(id) ON DELETE SET NULL,
ADD COLUMN IF NOT EXISTS scan_count INTEGER DEFAULT 1,  -- Número de veces que ha sido escaneado
ADD COLUMN IF NOT EXISTS verified BOOLEAN DEFAULT FALSE,  -- Si ha sido verificado por un nutriólogo
ADD COLUMN IF NOT EXISTS verified_by_user_id INTEGER REFERENCES auth_users(id) ON DELETE SET NULL,
ADD COLUMN IF NOT EXISTS verified_at TIMESTAMP WITH TIME ZONE,
ADD COLUMN IF NOT EXISTS is_global BOOLEAN DEFAULT TRUE,  -- Si es accesible globalmente
ADD COLUMN IF NOT EXISTS confidence_score FLOAT;  -- Score de confianza del Vision AI

-- Modificar la columna user_id para que sea nullable (ya que ahora los productos son globales)
ALTER TABLE productos_nom051
ALTER COLUMN user_id DROP NOT NULL;

-- Agregar comentarios
COMMENT ON COLUMN productos_nom051.image_hash IS 'Hash SHA-256 de la imagen de la etiqueta para deduplicación';
COMMENT ON COLUMN productos_nom051.created_by_user_id IS 'ID del usuario que creó este producto (primer escaneo)';
COMMENT ON COLUMN productos_nom051.scan_count IS 'Número de veces que este producto ha sido escaneado';
COMMENT ON COLUMN productos_nom051.verified IS 'Si el producto ha sido verificado manualmente por un nutriólogo';
COMMENT ON COLUMN productos_nom051.verified_by_user_id IS 'ID del nutriólogo que verificó este producto';
COMMENT ON COLUMN productos_nom051.verified_at IS 'Fecha y hora de verificación';
COMMENT ON COLUMN productos_nom051.is_global IS 'Si el producto es accesible globalmente (true) o privado (false)';
COMMENT ON COLUMN productos_nom051.confidence_score IS 'Score de confianza de la extracción de Vision AI (0-100)';

-- Índices para mejorar performance
CREATE INDEX IF NOT EXISTS idx_productos_nom051_image_hash ON productos_nom051(image_hash) WHERE image_hash IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_productos_nom051_created_by_user_id ON productos_nom051(created_by_user_id) WHERE created_by_user_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_productos_nom051_verified ON productos_nom051(verified);
CREATE INDEX IF NOT EXISTS idx_productos_nom051_is_global ON productos_nom051(is_global);
CREATE INDEX IF NOT EXISTS idx_productos_nom051_scan_count ON productos_nom051(scan_count DESC);

-- =====================================================
-- 2. Crear tabla de historial de escaneos por usuario
-- =====================================================

CREATE TABLE IF NOT EXISTS user_scan_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_users(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES productos_nom051(id) ON DELETE CASCADE,
    scan_type VARCHAR(20) NOT NULL CHECK (scan_type IN ('barcode', 'label', 'search')),
    scanned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    device_info JSONB,  -- Información del dispositivo (navegador, OS, etc.)
    location_context VARCHAR(100),  -- Contexto de ubicación (si está disponible)
    notes TEXT,  -- Notas personales del usuario sobre este producto

    -- Índices
    CONSTRAINT unique_user_product_scan UNIQUE(user_id, product_id, scanned_at)
);

-- Comentarios
COMMENT ON TABLE user_scan_history IS 'Historial personal de escaneos de cada usuario (privado)';
COMMENT ON COLUMN user_scan_history.scan_type IS 'Tipo de escaneo: barcode (código de barras), label (etiqueta con IA), search (búsqueda)';
COMMENT ON COLUMN user_scan_history.device_info IS 'Información del dispositivo usado para escanear (JSON)';
COMMENT ON COLUMN user_scan_history.location_context IS 'Contexto de ubicación (ej: supermercado, casa)';
COMMENT ON COLUMN user_scan_history.notes IS 'Notas personales del usuario sobre este producto';

-- Índices para historial
CREATE INDEX idx_user_scan_history_user_id ON user_scan_history(user_id);
CREATE INDEX idx_user_scan_history_product_id ON user_scan_history(product_id);
CREATE INDEX idx_user_scan_history_scanned_at ON user_scan_history(scanned_at DESC);
CREATE INDEX idx_user_scan_history_scan_type ON user_scan_history(scan_type);

-- Índice compuesto para consultas frecuentes
CREATE INDEX idx_user_scan_history_user_recent ON user_scan_history(user_id, scanned_at DESC);

-- =====================================================
-- 3. Crear tabla de imágenes de productos (opcional)
-- =====================================================

CREATE TABLE IF NOT EXISTS product_images (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES productos_nom051(id) ON DELETE CASCADE,
    image_url TEXT,
    image_data BYTEA,  -- Datos binarios de la imagen (opcional)
    image_hash VARCHAR(64) NOT NULL,
    image_type VARCHAR(20) CHECK (image_type IN ('label', 'front', 'back', 'ingredients')),
    uploaded_by_user_id INTEGER REFERENCES auth_users(id) ON DELETE SET NULL,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_primary BOOLEAN DEFAULT FALSE,

    -- Índices
    UNIQUE(image_hash)
);

COMMENT ON TABLE product_images IS 'Imágenes de productos escaneados (para deduplicación y referencia visual)';
COMMENT ON COLUMN product_images.image_hash IS 'Hash SHA-256 de la imagen para deduplicación';
COMMENT ON COLUMN product_images.image_type IS 'Tipo de imagen: label (etiqueta), front (frente), back (reverso), ingredients (ingredientes)';

CREATE INDEX idx_product_images_product_id ON product_images(product_id);
CREATE INDEX idx_product_images_image_hash ON product_images(image_hash);
CREATE INDEX idx_product_images_is_primary ON product_images(is_primary) WHERE is_primary = TRUE;

-- =====================================================
-- 4. Crear tabla de búsqueda de productos para IA
-- =====================================================

CREATE TABLE IF NOT EXISTS product_embeddings (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES productos_nom051(id) ON DELETE CASCADE,
    embedding_vector FLOAT8[],  -- Vector de embeddings para búsqueda semántica
    embedding_model VARCHAR(100),  -- Modelo usado para generar el embedding
    text_content TEXT,  -- Contenido de texto usado para generar el embedding
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    UNIQUE(product_id, embedding_model)
);

COMMENT ON TABLE product_embeddings IS 'Embeddings de productos para búsqueda semántica con IA (RAG)';
COMMENT ON COLUMN product_embeddings.embedding_vector IS 'Vector de embeddings para búsqueda de similitud';
COMMENT ON COLUMN product_embeddings.embedding_model IS 'Modelo de IA usado (ej: text-embedding-ada-002)';
COMMENT ON COLUMN product_embeddings.text_content IS 'Texto concatenado del producto usado para generar el embedding';

CREATE INDEX idx_product_embeddings_product_id ON product_embeddings(product_id);

-- =====================================================
-- 5. Crear vistas para consultas frecuentes
-- =====================================================

-- Vista de productos más escaneados (global)
CREATE OR REPLACE VIEW v_top_scanned_products AS
SELECT
    p.id,
    p.nombre,
    p.marca,
    p.codigo_barras,
    p.scan_count,
    p.fuente,
    p.health_score,
    p.health_level,
    p.verified,
    p.created_at,
    COUNT(DISTINCT ush.user_id) as unique_users_count
FROM productos_nom051 p
LEFT JOIN user_scan_history ush ON p.id = ush.product_id
WHERE p.is_global = TRUE
GROUP BY p.id
ORDER BY p.scan_count DESC, unique_users_count DESC
LIMIT 100;

COMMENT ON VIEW v_top_scanned_products IS 'Top 100 productos más escaneados globalmente';

-- Vista de historial personal del usuario
CREATE OR REPLACE VIEW v_user_scan_history AS
SELECT
    ush.id,
    ush.user_id,
    ush.scan_type,
    ush.scanned_at,
    ush.notes,
    p.id as product_id,
    p.nombre,
    p.marca,
    p.codigo_barras,
    p.health_score,
    p.health_level,
    p.exceso_calorias,
    p.exceso_azucares,
    p.exceso_grasas_saturadas,
    p.exceso_grasas_trans,
    p.exceso_sodio,
    p.contiene_edulcorantes,
    p.contiene_cafeina
FROM user_scan_history ush
JOIN productos_nom051 p ON ush.product_id = p.id
ORDER BY ush.scanned_at DESC;

COMMENT ON VIEW v_user_scan_history IS 'Historial de escaneos personalizado por usuario con información del producto';

-- Vista de productos verificados
CREATE OR REPLACE VIEW v_verified_products AS
SELECT
    p.*,
    u.email as verified_by_email,
    u.first_name as verified_by_first_name,
    u.last_name as verified_by_last_name
FROM productos_nom051 p
LEFT JOIN auth_users u ON p.verified_by_user_id = u.id
WHERE p.verified = TRUE AND p.is_global = TRUE;

COMMENT ON VIEW v_verified_products IS 'Productos verificados por nutriólogos';

-- =====================================================
-- 6. Función para registrar escaneo
-- =====================================================

CREATE OR REPLACE FUNCTION register_product_scan(
    p_user_id INTEGER,
    p_product_id INTEGER,
    p_scan_type VARCHAR(20),
    p_device_info JSONB DEFAULT NULL,
    p_location_context VARCHAR(100) DEFAULT NULL
)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    scan_history_id INTEGER;
BEGIN
    -- Incrementar contador de escaneos del producto
    UPDATE productos_nom051
    SET scan_count = scan_count + 1
    WHERE id = p_product_id;

    -- Registrar en historial personal del usuario
    INSERT INTO user_scan_history (
        user_id,
        product_id,
        scan_type,
        device_info,
        location_context,
        scanned_at
    ) VALUES (
        p_user_id,
        p_product_id,
        p_scan_type,
        p_device_info,
        p_location_context,
        NOW()
    )
    ON CONFLICT (user_id, product_id, scanned_at) DO NOTHING
    RETURNING id INTO scan_history_id;

    RETURN scan_history_id;
END;
$$;

COMMENT ON FUNCTION register_product_scan IS 'Registra un escaneo de producto en el historial del usuario e incrementa el contador global';

-- =====================================================
-- 7. Función para buscar productos similares (deduplicación)
-- =====================================================

CREATE OR REPLACE FUNCTION find_similar_products(
    p_nombre TEXT,
    p_marca TEXT,
    p_image_hash VARCHAR(64) DEFAULT NULL,
    p_limit INTEGER DEFAULT 5
)
RETURNS TABLE (
    product_id INTEGER,
    nombre TEXT,
    marca TEXT,
    similarity_score FLOAT,
    match_type VARCHAR(20)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    -- Buscar por hash de imagen (coincidencia exacta)
    SELECT
        p.id,
        p.nombre::TEXT,
        p.marca::TEXT,
        1.0 as similarity_score,
        'image_hash'::VARCHAR(20) as match_type
    FROM productos_nom051 p
    WHERE p.image_hash = p_image_hash AND p.image_hash IS NOT NULL

    UNION ALL

    -- Buscar por nombre y marca similares
    SELECT
        p.id,
        p.nombre::TEXT,
        p.marca::TEXT,
        GREATEST(
            similarity(p.nombre, p_nombre),
            similarity(p.marca, p_marca)
        ) as similarity_score,
        'text_similarity'::VARCHAR(20) as match_type
    FROM productos_nom051 p
    WHERE
        similarity(p.nombre, p_nombre) > 0.6
        OR similarity(p.marca, p_marca) > 0.7

    ORDER BY similarity_score DESC
    LIMIT p_limit;
END;
$$;

COMMENT ON FUNCTION find_similar_products IS 'Busca productos similares para deduplicación usando hash de imagen y similitud de texto';

-- Habilitar extensión pg_trgm si no está habilitada (para búsqueda de similitud)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- =====================================================
-- 8. Triggers para actualización automática
-- =====================================================

-- Trigger para actualizar updated_at en product_embeddings
CREATE OR REPLACE FUNCTION update_product_embeddings_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_product_embeddings_timestamp
    BEFORE UPDATE ON product_embeddings
    FOR EACH ROW
    EXECUTE FUNCTION update_product_embeddings_timestamp();

-- =====================================================
-- 9. Políticas de seguridad (Row Level Security)
-- =====================================================

-- Habilitar RLS en user_scan_history
ALTER TABLE user_scan_history ENABLE ROW LEVEL SECURITY;

-- Política: Los usuarios solo pueden ver su propio historial
CREATE POLICY user_scan_history_select_own
    ON user_scan_history
    FOR SELECT
    USING (user_id = current_setting('app.current_user_id')::INTEGER);

-- Política: Los usuarios solo pueden insertar en su propio historial
CREATE POLICY user_scan_history_insert_own
    ON user_scan_history
    FOR INSERT
    WITH CHECK (user_id = current_setting('app.current_user_id')::INTEGER);

-- Política: Los nutriólogos pueden ver historial de sus pacientes
-- (Esta política necesitará ser implementada cuando tengamos la relación nutritionist-patient)

-- =====================================================
-- 10. Insertar datos de ejemplo (opcional)
-- =====================================================

-- Actualizar productos existentes para que sean globales
UPDATE productos_nom051
SET
    is_global = TRUE,
    created_by_user_id = user_id,
    scan_count = 1
WHERE created_by_user_id IS NULL;

-- =====================================================
-- Fin de Migration 005
-- =====================================================

-- Verificar las nuevas tablas
SELECT 'Migration 005 completed successfully!' as status;

-- Mostrar resumen de cambios
SELECT
    'productos_nom051' as table_name,
    COUNT(*) as total_records,
    COUNT(*) FILTER (WHERE is_global = TRUE) as global_products,
    COUNT(*) FILTER (WHERE verified = TRUE) as verified_products
FROM productos_nom051
UNION ALL
SELECT
    'user_scan_history' as table_name,
    COUNT(*) as total_records,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(DISTINCT product_id) as unique_products
FROM user_scan_history;
