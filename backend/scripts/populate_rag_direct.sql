-- Populate RAG System with Sample Data
-- =====================================

-- Insert alimentos SMAE
INSERT INTO alimentos_smae (
    nombre, nombre_comun, grupo_smae, subgrupo, porcion, unidad_porcion, peso_neto_g,
    calorias, proteinas, carbohidratos, grasas, fibra, sodio_mg,
    es_mexicano, fuente, verificado, created_at, updated_at
) VALUES
('Tortilla de maíz', 'Tortilla', 'Cereales', 'Sin grasa', 30, 'g', 30, 64, 1.7, 13.4, 0.9, 1.5, 3, true, 'smae', true, NOW(), NOW()),
('Frijoles negros cocidos', 'Frijoles', 'Leguminosas', NULL, 120, 'g', 120, 120, 8, 20, 0.5, 7.5, 2, true, 'smae', true, NOW(), NOW()),
('Aguacate Hass', 'Aguacate', 'Grasas', 'Sin proteína', 30, 'g', 30, 45, 0.6, 2.4, 4.5, 2, 2, true, 'smae', true, NOW(), NOW()),
('Pollo pechuga sin piel', 'Pechuga de pollo', 'Alimentos de Origen Animal', 'Muy bajo aporte de grasa', 30, 'g', 30, 42, 7.5, 0, 1.5, NULL, 25, false, 'smae', true, NOW(), NOW()),
('Leche descremada', NULL, 'Leche', 'Descremada', 240, 'ml', 240, 95, 9, 12, 2, NULL, 130, false, 'smae', true, NOW(), NOW()),
('Nopal cocido', NULL, 'Verduras', NULL, 150, 'g', 150, 23, 1.5, 4, 0.1, 2.5, 2, true, 'smae', true, NOW(), NOW()),
('Mango manila', 'Mango', 'Frutas', NULL, 120, 'g', 120, 60, 0.5, 15, 0.2, 1.6, 1, true, 'smae', true, NOW(), NOW()),
('Chícharos cocidos', 'Chícharos', 'Leguminosas', NULL, 90, 'g', 90, 120, 8, 20, 0.5, 6, 4, false, 'smae', true, NOW(), NOW())
ON CONFLICT DO NOTHING;

-- Insert productos NOM-051
INSERT INTO productos_nom051 (
    codigo_barras, nombre, marca, porcion_gramos,
    calorias, proteinas, carbohidratos, azucares, grasas_totales, grasas_saturadas, grasas_trans, fibra, sodio,
    exceso_calorias, exceso_azucares, exceso_grasas_saturadas, exceso_grasas_trans, exceso_sodio,
    contiene_edulcorantes, contiene_cafeina,
    categoria, fuente, scan_count, verified, is_global, created_at, updated_at
) VALUES
('7501055300891', 'Coca-Cola Original', 'Coca-Cola', 100, 42, 0, 10.6, 10.6, 0, 0, 0, 0, 11, false, true, false, false, false, false, false, 'Bebidas', 'manual', 1, true, true, NOW(), NOW()),
('7501000111111', 'Sabritas Original', 'Sabritas', 30, 150, 2, 15, 1, 10, 1.5, 0, 1, 180, true, false, true, false, true, false, false, 'Botanas', 'manual', 1, true, true, NOW(), NOW()),
('7501234567890', 'Yogurt Griego Natural', 'Alpura', 100, 97, 10, 3.6, 3.6, 5, 3, 0, 0, 44, false, false, false, false, false, false, false, 'Lácteos', 'manual', 1, true, true, NOW(), NOW())
ON CONFLICT (codigo_barras) DO NOTHING;

SELECT 'Datos de ejemplo agregados correctamente' as status;
SELECT COUNT(*) as total_alimentos FROM alimentos_smae;
SELECT COUNT(*) as total_productos FROM productos_nom051;
