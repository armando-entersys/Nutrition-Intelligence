-- Import 26 NOM-051 products using direct SQL
-- Execute with: docker exec -i nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence -f /tmp/import_products_sql.sql

INSERT INTO productos_nom051 (
    codigo_barras, nombre, marca, porcion_gramos,
    calorias, proteinas, carbohidratos, azucares, grasas_totales, grasas_saturadas, grasas_trans, fibra, sodio,
    exceso_calorias, exceso_azucares, exceso_grasas_saturadas, exceso_grasas_trans, exceso_sodio,
    contiene_cafeina, contiene_edulcorantes,
    fuente, verified, is_global, scan_count, created_at, updated_at
) VALUES
-- BEBIDAS AZUCARADAS
('7501055300891', 'Coca-Cola Original', 'Coca-Cola', 100, 42, 0.0, 10.6, 10.6, 0.0, 0.0, 0.0, 0.0, 11, false, true, false, false, false, true, false, 'manual', true, true, 1, NOW(), NOW()),
('7501055362578', 'Coca-Cola Sin Azúcar', 'Coca-Cola', 100, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 15, false, false, false, false, false, true, true, 'manual', true, true, 1, NOW(), NOW()),
('7501055301294', 'Sprite', 'Coca-Cola', 100, 40, 0.0, 10.0, 10.0, 0.0, 0.0, 0.0, 0.0, 14, false, true, false, false, false, false, false, 'manual', true, true, 1, NOW(), NOW()),
('7501055303274', 'Fanta Naranja', 'Coca-Cola', 100, 47, 0.0, 11.8, 11.8, 0.0, 0.0, 0.0, 0.0, 12, false, true, false, false, false, false, false, 'manual', true, true, 1, NOW(), NOW()),
('7501055308859', 'Del Valle Manzana', 'Coca-Cola', 100, 45, 0.0, 11.0, 10.5, 0.0, 0.0, 0.0, 0.0, 8, false, true, false, false, false, false, false, 'manual', true, true, 1, NOW(), NOW()),

-- BOTANAS Y SNACKS
('7501055309122', 'Sabritas Clásicas', 'Sabritas', 100, 536, 6.3, 52.0, 2.0, 33.0, 11.0, 0.0, 4.5, 480, true, false, true, false, true, false, false, 'manual', true, true, 1, NOW(), NOW()),
('7501055309887', 'Cheetos Poffs', 'Sabritas', 100, 571, 5.7, 50.0, 5.7, 37.1, 10.0, 0.0, 2.9, 857, true, false, true, false, true, false, false, 'manual', true, true, 1, NOW(), NOW()),
('7501055310050', 'Doritos Nacho', 'Sabritas', 100, 500, 7.1, 60.7, 3.6, 25.0, 3.6, 0.0, 3.6, 536, true, false, false, false, true, false, false, 'manual', true, true, 1, NOW(), NOW()),
('7501055310548', 'Ruffles Queso', 'Sabritas', 100, 536, 6.3, 52.0, 3.0, 33.0, 11.0, 0.0, 4.0, 520, true, false, true, false, true, false, false, 'manual', true, true, 1, NOW(), NOW()),

-- CEREALES
('7501055311248', 'Zucaritas', 'Kellogg''s', 100, 380, 5.0, 85.0, 35.0, 1.0, 0.5, 0.0, 2.0, 200, true, true, false, false, false, false, false, 'manual', true, true, 1, NOW(), NOW()),
('7501055312245', 'Choco Krispis', 'Kellogg''s', 100, 387, 5.0, 83.0, 37.0, 3.0, 1.5, 0.0, 3.0, 333, true, true, false, false, false, false, false, 'manual', true, true, 1, NOW(), NOW()),
('7501055313242', 'Corn Flakes', 'Kellogg''s', 100, 357, 7.1, 84.3, 7.1, 0.0, 0.0, 0.0, 2.9, 643, true, false, false, false, true, false, false, 'manual', true, true, 1, NOW(), NOW()),

-- LÁCTEOS
('7501055314249', 'Yoghurt Griego Natural Alpura', 'Alpura', 100, 97, 10.0, 3.6, 3.6, 5.0, 3.2, 0.0, 0.0, 46, false, false, false, false, false, false, false, 'manual', true, true, 1, NOW(), NOW()),
('7501055315246', 'Yoghurt Griego Fresa Danone', 'Danone', 100, 124, 6.9, 16.9, 13.8, 2.6, 1.7, 0.0, 0.0, 43, false, true, false, false, false, false, false, 'manual', true, true, 1, NOW(), NOW()),

-- GALLETAS Y DULCES
('7501055316243', 'Oreo', 'Nabisco', 100, 480, 5.0, 70.0, 40.0, 20.0, 6.0, 0.0, 3.0, 380, true, true, true, false, false, false, false, 'manual', true, true, 1, NOW(), NOW()),
('7501055317240', 'Príncipe', 'Marinela', 100, 464, 5.4, 67.9, 33.9, 17.9, 8.9, 0.0, 1.8, 321, true, true, true, false, false, false, false, 'manual', true, true, 1, NOW(), NOW()),
('7501055318247', 'Gansito', 'Marinela', 100, 416, 4.9, 58.4, 36.8, 17.9, 8.4, 0.0, 1.1, 158, true, true, true, false, false, false, false, 'manual', true, true, 1, NOW(), NOW()),
('7501055319244', 'Submarinos', 'Marinela', 100, 446, 6.0, 64.0, 32.0, 18.0, 9.0, 0.0, 2.0, 280, true, true, true, false, false, false, false, 'manual', true, true, 1, NOW(), NOW()),

-- CHOCOLATE Y DULCERÍA
('7501055320241', 'Carlos V', 'Nestlé', 100, 534, 7.7, 57.7, 50.0, 30.8, 15.4, 0.0, 3.8, 115, true, true, true, false, false, true, false, 'manual', true, true, 1, NOW(), NOW()),
('7501055321248', 'KitKat', 'Nestlé', 100, 518, 6.5, 64.5, 48.4, 25.8, 16.1, 0.0, 1.6, 97, true, true, true, false, false, true, false, 'manual', true, true, 1, NOW(), NOW()),
('7501055322245', 'Milky Way', 'Mars', 100, 456, 4.4, 70.2, 56.1, 17.5, 10.5, 0.0, 0.9, 175, true, true, true, false, false, false, false, 'manual', true, true, 1, NOW(), NOW()),

-- COMIDA INSTANTÁNEA
('7501055323242', 'Maruchan Pollo', 'Maruchan', 100, 448, 9.0, 60.0, 2.0, 20.0, 10.0, 0.0, 2.0, 1800, true, false, true, false, true, false, false, 'manual', true, true, 1, NOW(), NOW()),
('7501055324249', 'Nissin Cup Noodles Camarón', 'Nissin', 100, 460, 9.5, 58.0, 2.5, 21.0, 10.5, 0.0, 2.5, 1950, true, false, true, false, true, false, false, 'manual', true, true, 1, NOW(), NOW()),

-- PRODUCTOS SALUDABLES (SIN SELLOS)
('7501055325246', 'Agua Natural Bonafont', 'Bonafont', 100, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, false, false, false, false, false, false, false, 'manual', true, true, 1, NOW(), NOW()),
('7501055326243', 'Almendras Natural Sin Sal', 'Great Value', 100, 607, 21.4, 21.4, 3.6, 50.0, 3.6, 0.0, 10.7, 0, false, false, false, false, false, false, false, 'manual', true, true, 1, NOW(), NOW()),
('7501055327240', 'Avena Natural Quaker', 'Quaker', 100, 379, 13.7, 67.7, 1.0, 6.5, 1.1, 0.0, 10.1, 6, false, false, false, false, false, false, false, 'manual', true, true, 1, NOW(), NOW())

;
