-- Import 48 SMAE foods using direct SQL
-- Execute with: docker exec -i nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence -f /tmp/import_smae_sql.sql

-- CEREALES SIN GRASA
INSERT INTO alimentos_smae (nombre, nombre_comun, grupo_smae, subgrupo, porcion, unidad_porcion, peso_neto_g, calorias, proteinas, carbohidratos, grasas, fibra, sodio_mg, es_mexicano, fuente, verificado, created_at, updated_at)
VALUES
('Tortilla de maíz', 'Tortilla', 'Cereales', 'Sin grasa', 30, 'g', 30, 64, 1.7, 13.4, 0.9, 1.5, 3, true, 'smae', true, NOW(), NOW()),
('Arroz cocido', 'Arroz blanco', 'Cereales', 'Sin grasa', 90, 'g', 90, 70, 2.0, 15.0, 0.0, 0.2, 1, false, 'smae', true, NOW(), NOW()),
('Pasta cocida', 'Pasta', 'Cereales', 'Sin grasa', 70, 'g', 70, 70, 2.5, 15.0, 0.2, 0.8, 1, false, 'smae', true, NOW(), NOW()),
('Pan de caja integral', 'Pan integral', 'Cereales', 'Sin grasa', 30, 'g', 30, 69, 2.6, 13.0, 1.0, 2.0, 150, false, 'smae', true, NOW(), NOW()),
('Avena cruda', 'Avena', 'Cereales', 'Sin grasa', 20, 'g', 20, 70, 2.6, 12.0, 1.4, 2.0, 1, false, 'smae', true, NOW(), NOW())
ON CONFLICT (nombre) DO NOTHING;

-- CEREALES CON GRASA
INSERT INTO alimentos_smae (nombre, nombre_comun, grupo_smae, subgrupo, porcion, unidad_porcion, peso_neto_g, calorias, proteinas, carbohidratos, grasas, fibra, sodio_mg, es_mexicano, fuente, verificado, created_at, updated_at)
VALUES
('Totopos', 'Totopos/Nachos', 'Cereales', 'Con grasa', 20, 'g', 20, 115, 2.0, 15.0, 5.0, 1.5, 150, true, 'smae', true, NOW(), NOW()),
('Pan dulce', 'Concha o pan dulce', 'Cereales', 'Con grasa', 40, 'g', 40, 115, 2.0, 15.0, 5.0, 0.5, 100, true, 'smae', true, NOW(), NOW())
ON CONFLICT (nombre) DO NOTHING;

-- FRUTAS
INSERT INTO alimentos_smae (nombre, nombre_comun, grupo_smae, subgrupo, porcion, unidad_porcion, peso_neto_g, calorias, proteinas, carbohidratos, grasas, fibra, sodio_mg, es_mexicano, fuente, verificado, created_at, updated_at)
VALUES
('Manzana con cáscara', 'Manzana', 'Frutas', 'General', 120, 'g', 120, 60, 0.0, 15.0, 0.0, 2.4, 1, false, 'smae', true, NOW(), NOW()),
('Plátano', 'Plátano Tabasco', 'Frutas', 'General', 80, 'g', 80, 60, 0.5, 15.0, 0.0, 1.6, 1, false, 'smae', true, NOW(), NOW()),
('Papaya', 'Papaya', 'Frutas', 'General', 150, 'g', 150, 60, 0.5, 15.0, 0.0, 1.8, 3, true, 'smae', true, NOW(), NOW()),
('Sandía', 'Sandía', 'Frutas', 'General', 250, 'g', 250, 60, 0.5, 15.0, 0.0, 1.0, 3, false, 'smae', true, NOW(), NOW()),
('Mango', 'Mango manila', 'Frutas', 'General', 120, 'g', 120, 60, 0.5, 15.0, 0.0, 1.8, 2, true, 'smae', true, NOW(), NOW()),
('Naranja', 'Naranja', 'Frutas', 'General', 150, 'g', 150, 60, 1.0, 15.0, 0.0, 2.4, 1, false, 'smae', true, NOW(), NOW()),
('Guayaba', 'Guayaba', 'Frutas', 'General', 110, 'g', 110, 60, 1.0, 15.0, 0.0, 5.5, 2, true, 'smae', true, NOW(), NOW())
ON CONFLICT (nombre) DO NOTHING;

-- VERDURAS
INSERT INTO alimentos_smae (nombre, nombre_comun, grupo_smae, subgrupo, porcion, unidad_porcion, peso_neto_g, calorias, proteinas, carbohidratos, grasas, fibra, sodio_mg, es_mexicano, fuente, verificado, created_at, updated_at)
VALUES
('Jitomate', 'Jitomate/Tomate rojo', 'Verduras', 'General', 150, 'g', 150, 25, 1.0, 5.0, 0.0, 1.5, 7, false, 'smae', true, NOW(), NOW()),
('Cebolla', 'Cebolla blanca', 'Verduras', 'General', 70, 'g', 70, 25, 0.7, 5.0, 0.0, 1.4, 3, false, 'smae', true, NOW(), NOW()),
('Calabacita', 'Calabacita italiana', 'Verduras', 'General', 150, 'g', 150, 25, 1.5, 5.0, 0.0, 1.5, 3, false, 'smae', true, NOW(), NOW()),
('Chayote', 'Chayote', 'Verduras', 'General', 150, 'g', 150, 25, 0.8, 5.0, 0.0, 2.0, 2, true, 'smae', true, NOW(), NOW()),
('Nopales', 'Nopal', 'Verduras', 'General', 150, 'g', 150, 25, 1.5, 5.0, 0.0, 3.0, 30, true, 'smae', true, NOW(), NOW()),
('Espinaca', 'Espinaca', 'Verduras', 'General', 150, 'g', 150, 25, 2.5, 5.0, 0.0, 2.5, 80, false, 'smae', true, NOW(), NOW()),
('Brócoli', 'Brócoli', 'Verduras', 'General', 100, 'g', 100, 25, 2.5, 5.0, 0.0, 2.4, 33, false, 'smae', true, NOW(), NOW())
ON CONFLICT (nombre) DO NOTHING;

-- LEGUMINOSAS
INSERT INTO alimentos_smae (nombre, nombre_comun, grupo_smae, subgrupo, porcion, unidad_porcion, peso_neto_g, calorias, proteinas, carbohidratos, grasas, fibra, sodio_mg, es_mexicano, fuente, verificado, created_at, updated_at)
VALUES
('Frijol negro cocido', 'Frijoles negros', 'Leguminosas', 'General', 80, 'g', 80, 120, 8.0, 20.0, 1.0, 7.5, 2, true, 'smae', true, NOW(), NOW()),
('Frijol pinto cocido', 'Frijoles pintos', 'Leguminosas', 'General', 80, 'g', 80, 120, 8.0, 20.0, 1.0, 7.0, 2, true, 'smae', true, NOW(), NOW()),
('Lentejas cocidas', 'Lentejas', 'Leguminosas', 'General', 80, 'g', 80, 120, 9.0, 20.0, 0.5, 8.0, 2, false, 'smae', true, NOW(), NOW()),
('Garbanzo cocido', 'Garbanzos', 'Leguminosas', 'General', 80, 'g', 80, 120, 8.0, 20.0, 2.0, 6.0, 7, false, 'smae', true, NOW(), NOW())
ON CONFLICT (nombre) DO NOTHING;

-- ALIMENTOS DE ORIGEN ANIMAL - MUY BAJO APORTE DE GRASA
INSERT INTO alimentos_smae (nombre, nombre_comun, grupo_smae, subgrupo, porcion, unidad_porcion, peso_neto_g, calorias, proteinas, carbohidratos, grasas, fibra, sodio_mg, es_mexicano, fuente, verificado, created_at, updated_at)
VALUES
('Pechuga de pollo sin piel', 'Pechuga de pollo', 'Alimentos de origen animal', 'Muy bajo aporte de grasa', 30, 'g', 30, 40, 7.0, 0.0, 1.0, 0.0, 20, false, 'smae', true, NOW(), NOW()),
('Pescado blanco', 'Pescado (tilapia, huachinango)', 'Alimentos de origen animal', 'Muy bajo aporte de grasa', 30, 'g', 30, 40, 7.0, 0.0, 1.0, 0.0, 30, false, 'smae', true, NOW(), NOW()),
('Clara de huevo', 'Clara de huevo', 'Alimentos de origen animal', 'Muy bajo aporte de grasa', 66, 'g', 66, 40, 7.0, 1.0, 0.0, 0.0, 55, false, 'smae', true, NOW(), NOW())
ON CONFLICT (nombre) DO NOTHING;

-- ALIMENTOS DE ORIGEN ANIMAL - BAJO APORTE DE GRASA
INSERT INTO alimentos_smae (nombre, nombre_comun, grupo_smae, subgrupo, porcion, unidad_porcion, peso_neto_g, calorias, proteinas, carbohidratos, grasas, fibra, sodio_mg, es_mexicano, fuente, verificado, created_at, updated_at)
VALUES
('Carne de res magra', 'Bistec de res', 'Alimentos de origen animal', 'Bajo aporte de grasa', 30, 'g', 30, 55, 7.0, 0.0, 3.0, 0.0, 20, false, 'smae', true, NOW(), NOW()),
('Huevo entero', 'Huevo', 'Alimentos de origen animal', 'Bajo aporte de grasa', 50, 'g', 50, 75, 7.0, 0.5, 5.0, 0.0, 70, false, 'smae', true, NOW(), NOW()),
('Atún en agua', 'Atún en lata', 'Alimentos de origen animal', 'Bajo aporte de grasa', 40, 'g', 40, 55, 7.0, 0.0, 3.0, 0.0, 200, false, 'smae', true, NOW(), NOW())
ON CONFLICT (nombre) DO NOTHING;

-- ALIMENTOS DE ORIGEN ANIMAL - MODERADO APORTE DE GRASA
INSERT INTO alimentos_smae (nombre, nombre_comun, grupo_smae, subgrupo, porcion, unidad_porcion, peso_neto_g, calorias, proteinas, carbohidratos, grasas, fibra, sodio_mg, es_mexicano, fuente, verificado, created_at, updated_at)
VALUES
('Carne molida de res', 'Carne molida', 'Alimentos de origen animal', 'Moderado aporte de grasa', 30, 'g', 30, 75, 7.0, 0.0, 5.0, 0.0, 20, false, 'smae', true, NOW(), NOW()),
('Queso panela', 'Queso panela', 'Alimentos de origen animal', 'Moderado aporte de grasa', 40, 'g', 40, 75, 7.0, 1.0, 5.0, 0.0, 180, true, 'smae', true, NOW(), NOW())
ON CONFLICT (nombre) DO NOTHING;

-- ALIMENTOS DE ORIGEN ANIMAL - ALTO APORTE DE GRASA
INSERT INTO alimentos_smae (nombre, nombre_comun, grupo_smae, subgrupo, porcion, unidad_porcion, peso_neto_g, calorias, proteinas, carbohidratos, grasas, fibra, sodio_mg, es_mexicano, fuente, verificado, created_at, updated_at)
VALUES
('Chorizo', 'Chorizo', 'Alimentos de origen animal', 'Alto aporte de grasa', 25, 'g', 25, 100, 7.0, 1.0, 8.0, 0.0, 300, true, 'smae', true, NOW(), NOW()),
('Queso Oaxaca', 'Quesillo', 'Alimentos de origen animal', 'Alto aporte de grasa', 30, 'g', 30, 100, 7.0, 1.0, 8.0, 0.0, 180, true, 'smae', true, NOW(), NOW())
ON CONFLICT (nombre) DO NOTHING;

-- LECHE
INSERT INTO alimentos_smae (nombre, nombre_comun, grupo_smae, subgrupo, porcion, unidad_porcion, peso_neto_g, calorias, proteinas, carbohidratos, grasas, fibra, sodio_mg, es_mexicano, fuente, verificado, created_at, updated_at)
VALUES
('Leche descremada', 'Leche Light', 'Leche', 'Descremada', 240, 'ml', 240, 95, 9.0, 12.0, 2.0, 0.0, 125, false, 'smae', true, NOW(), NOW()),
('Yogurt natural light', 'Yogurt bajo en grasa', 'Leche', 'Descremada', 240, 'ml', 240, 95, 9.0, 12.0, 2.0, 0.0, 150, false, 'smae', true, NOW(), NOW()),
('Leche semidescremada', 'Leche reducida en grasa', 'Leche', 'Semidescremada', 240, 'ml', 240, 110, 9.0, 12.0, 4.0, 0.0, 125, false, 'smae', true, NOW(), NOW()),
('Leche entera', 'Leche completa', 'Leche', 'Entera', 240, 'ml', 240, 150, 9.0, 12.0, 8.0, 0.0, 120, false, 'smae', true, NOW(), NOW())
ON CONFLICT (nombre) DO NOTHING;

-- ACEITES Y GRASAS
INSERT INTO alimentos_smae (nombre, nombre_comun, grupo_smae, subgrupo, porcion, unidad_porcion, peso_neto_g, calorias, proteinas, carbohidratos, grasas, fibra, sodio_mg, es_mexicano, fuente, verificado, created_at, updated_at)
VALUES
('Aceite vegetal', 'Aceite', 'Aceites y grasas', 'Sin proteína', 5, 'ml', 5, 45, 0.0, 0.0, 5.0, 0.0, 0, false, 'smae', true, NOW(), NOW()),
('Aguacate', 'Aguacate', 'Aceites y grasas', 'Con proteína', 30, 'g', 30, 45, 0.5, 2.5, 4.5, 2.0, 2, true, 'smae', true, NOW(), NOW()),
('Nuez', 'Nuez', 'Aceites y grasas', 'Con proteína', 10, 'g', 10, 70, 1.5, 1.5, 7.0, 0.7, 1, false, 'smae', true, NOW(), NOW()),
('Cacahuate', 'Cacahuate/Maní', 'Aceites y grasas', 'Con proteína', 10, 'g', 10, 60, 2.5, 2.0, 5.0, 1.0, 2, false, 'smae', true, NOW(), NOW())
ON CONFLICT (nombre) DO NOTHING;

-- AZÚCARES
INSERT INTO alimentos_smae (nombre, nombre_comun, grupo_smae, subgrupo, porcion, unidad_porcion, peso_neto_g, calorias, proteinas, carbohidratos, grasas, fibra, sodio_mg, es_mexicano, fuente, verificado, created_at, updated_at)
VALUES
('Azúcar blanca', 'Azúcar', 'Azúcares', 'Sin grasa', 10, 'g', 10, 40, 0.0, 10.0, 0.0, 0.0, 0, false, 'smae', true, NOW(), NOW()),
('Miel de abeja', 'Miel', 'Azúcares', 'Sin grasa', 10, 'g', 10, 40, 0.0, 10.0, 0.0, 0.0, 1, false, 'smae', true, NOW(), NOW()),
('Mermelada', 'Mermelada', 'Azúcares', 'Sin grasa', 15, 'g', 15, 40, 0.0, 10.0, 0.0, 0.2, 5, false, 'smae', true, NOW(), NOW()),
('Chocolate', 'Chocolate con leche', 'Azúcares', 'Con grasa', 10, 'g', 10, 60, 1.0, 6.0, 3.5, 0.5, 15, false, 'smae', true, NOW(), NOW()),
('Cajeta', 'Cajeta', 'Azúcares', 'Con grasa', 15, 'g', 15, 60, 1.0, 11.0, 1.5, 0.0, 35, true, 'smae', true, NOW(), NOW())
ON CONFLICT (nombre) DO NOTHING;
