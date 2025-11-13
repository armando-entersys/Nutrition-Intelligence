-- Migración 010: Productos y Tiendas Bienestar
-- Apoyo a iniciativas del Gobierno de México - Alimentación para el Bienestar
-- Fecha: Noviembre 2025

-- Tabla de Productos Bienestar (Marca del Gobierno)
CREATE TABLE IF NOT EXISTS productos_bienestar (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(100) NOT NULL, -- maiz, frijol, arroz, cacao, cafe, miel, canasta_basica

    -- Precios
    precio_productor DECIMAL(10, 2), -- precio justo pagado a productores
    precio_publico DECIMAL(10, 2), -- precio al público en tiendas
    precio_canasta DECIMAL(10, 2), -- si es parte de canasta (450 pesos)

    -- Origen y Productores
    origen_estado VARCHAR(100), -- estado productor principal
    origen_municipio VARCHAR(150),
    productor_tipo VARCHAR(50) CHECK (productor_tipo IN ('pequeño', 'mediano', 'cooperativa', 'ejido')),
    nombre_cooperativa VARCHAR(255),

    -- Certificaciones
    certificacion_organica BOOLEAN DEFAULT FALSE,
    certificacion_calidad BOOLEAN DEFAULT FALSE,
    certificacion_comercio_justo BOOLEAN DEFAULT FALSE,

    -- Información Nutricional
    info_nutricional JSONB, -- calorias, proteinas, carbohidratos, etc.
    porcion_gramos INTEGER,
    porciones_por_envase INTEGER,

    -- Cumplimiento NOM-051
    cumple_nom051 BOOLEAN DEFAULT TRUE,
    tiene_sellos BOOLEAN DEFAULT FALSE,
    sellos_advertencia JSONB, -- array de sellos si aplica

    -- Disponibilidad
    disponible_tiendas_bienestar BOOLEAN DEFAULT TRUE,
    disponible_todo_año BOOLEAN DEFAULT TRUE,
    temporada_inicio INTEGER, -- mes inicio (1-12)
    temporada_fin INTEGER, -- mes fin (1-12)

    -- Identificación
    codigo_barras VARCHAR(50) UNIQUE,
    sku VARCHAR(50),

    -- Trazabilidad
    fecha_cosecha DATE,
    lote_produccion VARCHAR(50),

    -- Metadata
    imagen_url TEXT,
    es_valor_agregado BOOLEAN DEFAULT FALSE, -- productos transformados marca Bienestar
    proceso_transformacion TEXT, -- ej: "tostado y molido de café"

    -- Control
    activo BOOLEAN DEFAULT TRUE,
    verificado_por VARCHAR(255), -- usuario que verificó
    verificado_fecha TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de Tiendas Bienestar (25,600 establecimientos)
CREATE TABLE IF NOT EXISTS tiendas_bienestar (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    codigo_tienda VARCHAR(50) UNIQUE NOT NULL, -- código oficial gobierno

    -- Ubicación
    estado VARCHAR(100) NOT NULL,
    municipio VARCHAR(150) NOT NULL,
    localidad VARCHAR(150),
    colonia VARCHAR(150),
    calle VARCHAR(255),
    numero_exterior VARCHAR(20),
    numero_interior VARCHAR(20),
    codigo_postal VARCHAR(10),

    -- Geolocalización
    latitud DECIMAL(10, 7),
    longitud DECIMAL(10, 7),

    -- Contacto
    telefono VARCHAR(20),
    email VARCHAR(255),
    encargado_nombre VARCHAR(255),

    -- Operación
    horario_apertura TIME,
    horario_cierre TIME,
    dias_operacion VARCHAR(50), -- "Lunes a Sábado"
    tipo_tienda VARCHAR(50) CHECK (tipo_tienda IN ('fija', 'móvil', 'comunitaria')),

    -- Servicios
    acepta_tarjeta BOOLEAN DEFAULT FALSE,
    tiene_estacionamiento BOOLEAN DEFAULT FALSE,
    accesible_discapacidad BOOLEAN DEFAULT FALSE,

    -- Productos disponibles (referencia rápida)
    productos_disponibles INTEGER DEFAULT 0,
    tiene_canasta_basica BOOLEAN DEFAULT TRUE,

    -- Metadata
    foto_fachada_url TEXT,

    -- Control
    activa BOOLEAN DEFAULT TRUE,
    fecha_apertura DATE,
    ultima_inspeccion DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de relación: Disponibilidad de productos en tiendas
CREATE TABLE IF NOT EXISTS tienda_disponibilidad (
    id SERIAL PRIMARY KEY,
    tienda_id INTEGER REFERENCES tiendas_bienestar(id) ON DELETE CASCADE,
    producto_id INTEGER REFERENCES productos_bienestar(id) ON DELETE CASCADE,

    -- Stock
    stock INTEGER DEFAULT 0,
    stock_minimo INTEGER DEFAULT 10,
    stock_maximo INTEGER DEFAULT 100,

    -- Precio específico de tienda (puede variar ligeramente)
    precio_actual DECIMAL(10, 2),

    -- Control
    ultima_reposicion DATE,
    proxima_entrega DATE,
    disponible BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMP DEFAULT NOW(),

    -- Constraint único: un producto solo puede estar una vez por tienda
    UNIQUE(tienda_id, producto_id)
);

-- Tabla de ventas/consumo (para analytics)
CREATE TABLE IF NOT EXISTS ventas_productos_bienestar (
    id SERIAL PRIMARY KEY,
    tienda_id INTEGER REFERENCES tiendas_bienestar(id),
    producto_id INTEGER REFERENCES productos_bienestar(id),
    cantidad INTEGER NOT NULL,
    precio_venta DECIMAL(10, 2) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    fecha_venta TIMESTAMP DEFAULT NOW(),

    -- Si el usuario está logueado (opcional)
    usuario_id INTEGER REFERENCES users(id),

    -- Método de pago
    metodo_pago VARCHAR(50) CHECK (metodo_pago IN ('efectivo', 'tarjeta', 'vale', 'otro'))
);

-- Índices para mejor performance
CREATE INDEX idx_productos_bienestar_categoria ON productos_bienestar(categoria);
CREATE INDEX idx_productos_bienestar_estado ON productos_bienestar(origen_estado);
CREATE INDEX idx_productos_bienestar_codigo ON productos_bienestar(codigo_barras);
CREATE INDEX idx_productos_bienestar_activo ON productos_bienestar(activo);
CREATE INDEX idx_productos_bienestar_disponible ON productos_bienestar(disponible_tiendas_bienestar);

CREATE INDEX idx_tiendas_bienestar_estado ON tiendas_bienestar(estado);
CREATE INDEX idx_tiendas_bienestar_municipio ON tiendas_bienestar(municipio);
CREATE INDEX idx_tiendas_bienestar_codigo ON tiendas_bienestar(codigo_tienda);
CREATE INDEX idx_tiendas_bienestar_activa ON tiendas_bienestar(activa);
CREATE INDEX idx_tiendas_bienestar_location ON tiendas_bienestar(latitud, longitud);

CREATE INDEX idx_tienda_disponibilidad_tienda ON tienda_disponibilidad(tienda_id);
CREATE INDEX idx_tienda_disponibilidad_producto ON tienda_disponibilidad(producto_id);
CREATE INDEX idx_tienda_disponibilidad_disponible ON tienda_disponibilidad(disponible);

CREATE INDEX idx_ventas_fecha ON ventas_productos_bienestar(fecha_venta);
CREATE INDEX idx_ventas_tienda ON ventas_productos_bienestar(tienda_id);
CREATE INDEX idx_ventas_producto ON ventas_productos_bienestar(producto_id);

-- Función para calcular distancia entre coordenadas (Haversine)
CREATE OR REPLACE FUNCTION calcular_distancia(
    lat1 DECIMAL, lon1 DECIMAL, lat2 DECIMAL, lon2 DECIMAL
) RETURNS DECIMAL AS $$
DECLARE
    R DECIMAL := 6371; -- Radio de la Tierra en km
    dLat DECIMAL;
    dLon DECIMAL;
    a DECIMAL;
    c DECIMAL;
BEGIN
    dLat := RADIANS(lat2 - lat1);
    dLon := RADIANS(lon2 - lon1);

    a := SIN(dLat/2) * SIN(dLat/2) +
         COS(RADIANS(lat1)) * COS(RADIANS(lat2)) *
         SIN(dLon/2) * SIN(dLon/2);

    c := 2 * ATAN2(SQRT(a), SQRT(1-a));

    RETURN R * c;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Vista para productos más vendidos por estado
CREATE OR REPLACE VIEW productos_bienestar_top_por_estado AS
SELECT
    t.estado,
    pb.nombre AS producto,
    pb.categoria,
    COUNT(v.id) AS total_ventas,
    SUM(v.cantidad) AS cantidad_total,
    SUM(v.total) AS ingresos_totales
FROM ventas_productos_bienestar v
JOIN tiendas_bienestar t ON v.tienda_id = t.id
JOIN productos_bienestar pb ON v.producto_id = pb.id
GROUP BY t.estado, pb.id, pb.nombre, pb.categoria
ORDER BY t.estado, total_ventas DESC;

-- Vista para tiendas con bajo stock
CREATE OR REPLACE VIEW tiendas_con_stock_bajo AS
SELECT
    t.id AS tienda_id,
    t.nombre AS tienda,
    t.estado,
    t.municipio,
    pb.nombre AS producto,
    td.stock,
    td.stock_minimo,
    td.ultima_reposicion
FROM tienda_disponibilidad td
JOIN tiendas_bienestar t ON td.tienda_id = t.id
JOIN productos_bienestar pb ON td.producto_id = pb.id
WHERE td.stock < td.stock_minimo
  AND td.disponible = TRUE
  AND t.activa = TRUE
ORDER BY t.estado, t.municipio, td.stock;

-- Trigger para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_productos_bienestar_updated_at BEFORE UPDATE ON productos_bienestar
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tiendas_bienestar_updated_at BEFORE UPDATE ON tiendas_bienestar
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tienda_disponibilidad_updated_at BEFORE UPDATE ON tienda_disponibilidad
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comentarios para documentación
COMMENT ON TABLE productos_bienestar IS 'Productos de la marca Bienestar del gobierno federal';
COMMENT ON TABLE tiendas_bienestar IS '25,600 Tiendas Bienestar a nivel nacional (2025)';
COMMENT ON TABLE tienda_disponibilidad IS 'Control de inventario de productos en tiendas';
COMMENT ON TABLE ventas_productos_bienestar IS 'Registro de ventas para analytics gubernamentales';

COMMENT ON COLUMN productos_bienestar.precio_productor IS 'Precio justo pagado al productor sin intermediarios';
COMMENT ON COLUMN productos_bienestar.precio_publico IS 'Precio al público en Tiendas Bienestar';
COMMENT ON COLUMN productos_bienestar.es_valor_agregado IS 'Producto transformado (ej: café molido, cacao en polvo)';
COMMENT ON COLUMN tiendas_bienestar.codigo_tienda IS 'Código oficial asignado por el gobierno federal';

-- Datos iniciales de ejemplo (categorías base)
INSERT INTO productos_bienestar (nombre, categoria, precio_publico, cumple_nom051, disponible_tiendas_bienestar) VALUES
('Maíz Blanco Grano (Kg)', 'maiz', 20.00, TRUE, TRUE),
('Frijol Negro (Kg)', 'frijol', 35.00, TRUE, TRUE),
('Frijol Pinto (Kg)', 'frijol', 32.00, TRUE, TRUE),
('Arroz Integral (Kg)', 'arroz', 28.00, TRUE, TRUE),
('Café Orgánico Molido (500g)', 'cafe', 85.00, TRUE, TRUE),
('Miel de Abeja Natural (500g)', 'miel', 120.00, TRUE, TRUE),
('Cacao en Polvo Natural (250g)', 'cacao', 65.00, TRUE, TRUE)
ON CONFLICT (codigo_barras) DO NOTHING;

COMMIT;
