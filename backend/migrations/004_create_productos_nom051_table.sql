-- Migration: Tabla productos_nom051 para Escáner NOM-051
-- Descripción: Almacena información de productos escaneados con código de barras
--              incluyendo datos nutricionales y sellos de advertencia NOM-051
-- Fecha: 2025-11-09

-- Tabla principal de productos NOM-051
CREATE TABLE IF NOT EXISTS productos_nom051 (
    id SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    marca VARCHAR(255),

    -- Información nutricional (por 100g/ml)
    porcion_gramos DECIMAL(10,2),
    calorias DECIMAL(10,2),
    proteinas DECIMAL(10,2),
    carbohidratos DECIMAL(10,2),
    azucares DECIMAL(10,2),
    grasas_totales DECIMAL(10,2),
    grasas_saturadas DECIMAL(10,2),
    grasas_trans DECIMAL(10,2),
    fibra DECIMAL(10,2),
    sodio DECIMAL(10,2), -- en mg

    -- Sellos NOM-051 (calculados según criterios oficiales)
    exceso_calorias BOOLEAN DEFAULT FALSE,
    exceso_azucares BOOLEAN DEFAULT FALSE,
    exceso_grasas_saturadas BOOLEAN DEFAULT FALSE,
    exceso_grasas_trans BOOLEAN DEFAULT FALSE,
    exceso_sodio BOOLEAN DEFAULT FALSE,
    contiene_edulcorantes BOOLEAN DEFAULT FALSE,
    contiene_cafeina BOOLEAN DEFAULT FALSE,

    -- Metadatos del producto
    fuente VARCHAR(50) NOT NULL, -- 'open_food_facts', 'manual', 'ai_vision'
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id INTEGER REFERENCES auth_users(id) ON DELETE SET NULL,
    validado BOOLEAN DEFAULT FALSE,

    -- Información adicional
    imagen_url TEXT,
    ingredientes TEXT,
    categoria VARCHAR(100),
    pais_origen VARCHAR(100),

    -- Datos Open Food Facts (si aplica)
    openfoodfacts_id VARCHAR(50),

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT valid_barcode CHECK (LENGTH(codigo_barras) >= 8 AND LENGTH(codigo_barras) <= 20),
    CONSTRAINT valid_fuente CHECK (fuente IN ('open_food_facts', 'manual', 'ai_vision'))
);

-- Índices para búsqueda rápida
CREATE INDEX IF NOT EXISTS idx_productos_nom051_barcode ON productos_nom051(codigo_barras);
CREATE INDEX IF NOT EXISTS idx_productos_nom051_marca ON productos_nom051(marca);
CREATE INDEX IF NOT EXISTS idx_productos_nom051_categoria ON productos_nom051(categoria);
CREATE INDEX IF NOT EXISTS idx_productos_nom051_fuente ON productos_nom051(fuente);
CREATE INDEX IF NOT EXISTS idx_productos_nom051_validado ON productos_nom051(validado);
CREATE INDEX IF NOT EXISTS idx_productos_nom051_created_at ON productos_nom051(created_at DESC);

-- Índices para búsqueda de texto
CREATE INDEX IF NOT EXISTS idx_productos_nom051_nombre ON productos_nom051 USING gin(to_tsvector('spanish', nombre));
CREATE INDEX IF NOT EXISTS idx_productos_nom051_ingredientes ON productos_nom051 USING gin(to_tsvector('spanish', ingredientes));

-- Tabla de historial de escaneos (analytics)
CREATE TABLE IF NOT EXISTS escaneos_historia (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES auth_users(id) ON DELETE CASCADE,
    producto_id INTEGER REFERENCES productos_nom051(id) ON DELETE SET NULL,
    codigo_barras VARCHAR(20) NOT NULL,
    encontrado BOOLEAN NOT NULL,
    fuente VARCHAR(50), -- 'cache_local', 'open_food_facts', 'ai_vision', 'manual'
    tiempo_respuesta_ms INTEGER, -- tiempo que tomó encontrar el producto
    fecha_escaneo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Información del dispositivo (útil para analytics)
    dispositivo VARCHAR(100), -- 'mobile', 'desktop', 'tablet'
    navegador VARCHAR(100)
);

-- Índices para analytics
CREATE INDEX IF NOT EXISTS idx_escaneos_usuario ON escaneos_historia(usuario_id);
CREATE INDEX IF NOT EXISTS idx_escaneos_fecha ON escaneos_historia(fecha_escaneo DESC);
CREATE INDEX IF NOT EXISTS idx_escaneos_producto ON escaneos_historia(producto_id);
CREATE INDEX IF NOT EXISTS idx_escaneos_encontrado ON escaneos_historia(encontrado);
CREATE INDEX IF NOT EXISTS idx_escaneos_fuente ON escaneos_historia(fuente);

-- Índice compuesto para queries comunes
CREATE INDEX IF NOT EXISTS idx_escaneos_usuario_fecha ON escaneos_historia(usuario_id, fecha_escaneo DESC);

-- Trigger para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_productos_nom051_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_productos_nom051_timestamp
    BEFORE UPDATE ON productos_nom051
    FOR EACH ROW
    EXECUTE FUNCTION update_productos_nom051_updated_at();

-- Comentarios en las tablas
COMMENT ON TABLE productos_nom051 IS 'Almacena información de productos escaneados con código de barras y sellos NOM-051';
COMMENT ON TABLE escaneos_historia IS 'Registro de todos los escaneos realizados por usuarios para analytics';

COMMENT ON COLUMN productos_nom051.codigo_barras IS 'Código de barras EAN-13, UPC-A, o similar';
COMMENT ON COLUMN productos_nom051.fuente IS 'Origen de los datos: open_food_facts, manual, o ai_vision';
COMMENT ON COLUMN productos_nom051.validado IS 'Indica si el producto fue validado por un nutriólogo o administrador';
COMMENT ON COLUMN productos_nom051.exceso_calorias IS 'Sello NOM-051: Exceso de calorías según tabla oficial';
COMMENT ON COLUMN productos_nom051.exceso_azucares IS 'Sello NOM-051: Exceso de azúcares según tabla oficial';
COMMENT ON COLUMN productos_nom051.exceso_grasas_saturadas IS 'Sello NOM-051: Exceso de grasas saturadas según tabla oficial';
COMMENT ON COLUMN productos_nom051.exceso_grasas_trans IS 'Sello NOM-051: Exceso de grasas trans según tabla oficial';
COMMENT ON COLUMN productos_nom051.exceso_sodio IS 'Sello NOM-051: Exceso de sodio según tabla oficial';

-- Insertar datos demo (opcional - remover en producción)
INSERT INTO productos_nom051 (
    codigo_barras, nombre, marca, porcion_gramos, calorias, proteinas, carbohidratos,
    azucares, grasas_totales, grasas_saturadas, grasas_trans, fibra, sodio,
    exceso_calorias, exceso_azucares, exceso_grasas_saturadas, exceso_grasas_trans, exceso_sodio,
    contiene_edulcorantes, contiene_cafeina, fuente, categoria, validado
) VALUES
(
    '7501234567890',
    'Refresco de Cola Regular',
    'Demo Brand',
    100,  -- 100ml
    42,   -- kcal
    0,    -- proteínas
    10.6, -- carbohidratos
    10.6, -- azúcares
    0,    -- grasas totales
    0,    -- grasas saturadas
    0,    -- grasas trans
    0,    -- fibra
    11,   -- sodio (mg)
    FALSE, -- exceso_calorias
    TRUE,  -- exceso_azucares
    FALSE, -- exceso_grasas_saturadas
    FALSE, -- exceso_grasas_trans
    FALSE, -- exceso_sodio
    FALSE, -- contiene_edulcorantes
    TRUE,  -- contiene_cafeina
    'manual',
    'BEVERAGES',
    TRUE
),
(
    '7509876543210',
    'Galletas con Chispas de Chocolate',
    'Demo Brand',
    30,   -- 30g (porción)
    150,  -- kcal
    2,    -- proteínas
    20,   -- carbohidratos
    12,   -- azúcares
    7,    -- grasas totales
    3.5,  -- grasas saturadas
    0,    -- grasas trans
    1,    -- fibra
    85,   -- sodio (mg)
    TRUE,  -- exceso_calorias
    TRUE,  -- exceso_azucares
    TRUE,  -- exceso_grasas_saturadas
    FALSE, -- exceso_grasas_trans
    TRUE,  -- exceso_sodio
    FALSE, -- contiene_edulcorantes
    FALSE, -- contiene_cafeina
    'manual',
    'CEREALS',
    TRUE
);

-- Mensaje de éxito
DO $$
BEGIN
    RAISE NOTICE '✅ Migración 004: Tablas productos_nom051 y escaneos_historia creadas exitosamente';
    RAISE NOTICE '📊 2 productos demo insertados para pruebas';
    RAISE NOTICE '🔍 Índices creados para búsqueda optimizada';
    RAISE NOTICE '⚙️ Trigger de updated_at configurado';
END $$;
