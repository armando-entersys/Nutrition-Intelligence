"""
Script para scrape TODOS los alimentos del SMAE por grupos
https://midietasmae.com.mx/Manager/Grupo/Default.aspx

Itera sobre cada grupo en el dropdown y extrae todos los alimentos con información completa
"""
import sys
import os
import json
import time
import re
import psycopg2
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Credenciales de acceso
LOGIN_URL = "https://midietasmae.com.mx/Manager/Grupo/Default.aspx"
EMAIL = "ajcortest@gmail.com"
PASSWORD = "Lisa01183116"

# Mapeo de categorías SMAE a categorías del sistema (UPPERCASE para PostgreSQL)
CATEGORY_MAP = {
    'cereales sin grasa': 'CEREALS',
    'cereales con grasa': 'CEREALS',
    'leguminosas': 'LEGUMES',
    'verduras': 'VEGETABLES',
    'frutas': 'FRUITS',
    'leche descremada': 'DAIRY',
    'leche semidescremada': 'DAIRY',
    'leche entera': 'DAIRY',
    'carnes muy bajo aporte': 'ANIMAL_PRODUCTS',
    'carnes bajo aporte': 'ANIMAL_PRODUCTS',
    'carnes moderado aporte': 'ANIMAL_PRODUCTS',
    'carnes alto aporte': 'ANIMAL_PRODUCTS',
    'grasas sin proteina': 'FATS',
    'grasas con proteina': 'FATS',
    'azucares sin grasa': 'SUGARS',
    'azucares con grasa': 'SUGARS',
    'bebida libre': 'BEVERAGES',
    'aceites': 'FATS',
    'alimentos libres': 'FREE_FOODS'
}

def scrape_all_groups():
    """Scrape todos los grupos de alimentos desde SMAE"""

    print("🌐 Iniciando scraping completo de SMAE...")
    print(f"URL: {LOGIN_URL}")

    all_foods_by_group = {}

    with sync_playwright() as p:
        # Lanzar navegador
        print("\n🚀 Lanzando navegador Chromium...")
        browser = p.chromium.launch(
            headless=False,  # Mostrar navegador para ver qué pasa
            slow_mo=1000  # Más lento para debugging
        )

        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()

        try:
            # ============================================
            # PASO 1: LOGIN
            # ============================================
            print(f"\n📍 Navegando a {LOGIN_URL}...")
            page.goto(LOGIN_URL, wait_until='networkidle', timeout=30000)
            time.sleep(2)

            # Guardar screenshot inicial
            page.screenshot(path="screenshot_01_login.png")
            print("📸 Screenshot guardado: screenshot_01_login.png")

            # Guardar HTML para analizar la estructura ASP.NET
            with open('login_page.html', 'w', encoding='utf-8') as f:
                f.write(page.content())
            print("📄 HTML guardado: login_page.html")

            # Intentar diferentes estrategias de login
            print("\n🔍 Buscando formulario de login...")

            # Buscar todos los inputs
            inputs = page.locator('input').all()
            print(f"Encontrados {len(inputs)} campos input")

            email_input = None
            password_input = None

            for inp in inputs:
                try:
                    input_id = inp.get_attribute('id') or ''
                    input_type = inp.get_attribute('type') or ''
                    input_name = inp.get_attribute('name') or ''

                    # Buscar campo de email/usuario
                    if any(x in input_id.lower() + input_name.lower() for x in ['email', 'usuario', 'user', 'login']):
                        if input_type != 'password':
                            email_input = inp
                            print(f"✅ Campo email encontrado: {input_id or input_name}")

                    # Buscar campo de contraseña
                    if input_type == 'password':
                        password_input = inp
                        print(f"✅ Campo password encontrado: {input_id or input_name}")

                except Exception as e:
                    continue

            if not email_input or not password_input:
                print("❌ No se encontraron campos de login")
                print("Revisa login_page.html para identificar los campos correctos")
                return {}

            # Llenar formulario
            print(f"\n📝 Llenando formulario de login...")
            email_input.fill(EMAIL)
            print(f"  ✅ Email: {EMAIL}")

            password_input.fill(PASSWORD)
            print(f"  ✅ Password ingresado")

            # Buscar botón de submit
            print("\n🔍 Buscando botón de submit...")
            buttons = page.locator('input[type="submit"], input[type="button"], button').all()

            submit_button = None
            for btn in buttons:
                try:
                    btn_value = btn.get_attribute('value') or btn.inner_text() or ''
                    btn_id = btn.get_attribute('id') or ''

                    if any(x in btn_value.lower() + btn_id.lower() for x in ['iniciar', 'entrar', 'login', 'ingresar', 'acceder']):
                        submit_button = btn
                        print(f"✅ Botón encontrado: {btn_value or btn_id}")
                        break
                except:
                    continue

            if not submit_button:
                print("❌ No se encontró botón de submit")
                return {}

            # Hacer login
            print("\n🔐 Haciendo login...")

            # Tomar screenshot antes del click
            page.screenshot(path="screenshot_02_before_submit.png")

            # Click en el botón (puede que no sea visible, intentar force=True)
            try:
                submit_button.click(timeout=5000)
            except:
                print("⚠️ Click normal falló, intentando con force=True...")
                submit_button.click(force=True)

            # Esperar navegación
            try:
                page.wait_for_load_state('networkidle', timeout=15000)
            except:
                print("⏱️ Timeout en navegación, continuando...")

            time.sleep(3)

            # Verificar login exitoso
            current_url = page.url
            print(f"\n📍 URL después de login: {current_url}")

            page.screenshot(path="screenshot_03_after_login.png")
            print("📸 Screenshot después de login: screenshot_03_after_login.png")

            # ============================================
            # PASO 2: ENCONTRAR DROPDOWN DE GRUPOS
            # ============================================
            print("\n🔍 Buscando dropdown de grupos...")

            # Buscar select dropdown
            selects = page.locator('select').all()
            print(f"Encontrados {len(selects)} elementos select")

            group_select = None
            for sel in selects:
                try:
                    sel_id = sel.get_attribute('id') or ''
                    sel_name = sel.get_attribute('name') or ''

                    if 'grup' in sel_id.lower() + sel_name.lower():
                        group_select = sel
                        print(f"✅ Dropdown de grupos encontrado: {sel_id or sel_name}")
                        break
                except:
                    continue

            if not group_select:
                # Intentar con el primer select
                if len(selects) > 0:
                    group_select = selects[0]
                    print("⚠️ Usando el primer select encontrado")
                else:
                    print("❌ No se encontró dropdown de grupos")
                    with open('after_login.html', 'w', encoding='utf-8') as f:
                        f.write(page.content())
                    print("📄 HTML guardado: after_login.html")
                    return {}

            # Obtener todas las opciones del dropdown
            options = group_select.locator('option').all()
            print(f"\n📋 Encontradas {len(options)} opciones en el dropdown:")

            group_options = []
            for i, opt in enumerate(options):
                try:
                    value = opt.get_attribute('value') or ''
                    text = opt.inner_text() or ''

                    # Saltar opciones vacías o de selección
                    if value and value != '0' and 'seleccione' not in text.lower():
                        group_options.append({'value': value, 'text': text})
                        print(f"  {i}. {text} (value={value})")
                except:
                    continue

            print(f"\n✅ Total de grupos a procesar: {len(group_options)}")

            # ============================================
            # PASO 3: ITERAR SOBRE CADA GRUPO
            # ============================================
            for idx, group in enumerate(group_options, 1):
                group_name = group['text']
                group_value = group['value']

                print(f"\n{'='*60}")
                print(f"📦 Grupo {idx}/{len(group_options)}: {group_name}")
                print(f"{'='*60}")

                try:
                    # Seleccionar el grupo
                    print(f"🔄 Seleccionando grupo '{group_name}'...")
                    group_select.select_option(value=group_value)

                    # Esperar a que cargue la tabla
                    time.sleep(2)

                    # Esperar a que aparezca la tabla
                    try:
                        page.wait_for_selector('table', timeout=5000)
                    except:
                        print(f"⚠️ No se encontró tabla para el grupo {group_name}")
                        continue

                    # Tomar screenshot del grupo
                    page.screenshot(path=f"screenshot_group_{idx}_{group_name.replace(' ', '_')}.png")

                    # Buscar tabla de alimentos
                    tables = page.locator('table').all()

                    if not tables:
                        print(f"❌ No se encontró tabla para {group_name}")
                        continue

                    # Usar la primera tabla (o buscar por ID)
                    table = tables[0]

                    # Extraer filas
                    rows = table.locator('tr').all()
                    print(f"📊 Encontradas {len(rows)} filas")

                    group_foods = []

                    # Procesar cada fila (saltar header)
                    for row_idx, row in enumerate(rows[1:], 1):
                        try:
                            cells = row.locator('td').all()

                            if len(cells) < 2:
                                continue

                            # Extraer datos de las celdas
                            food_data = {
                                'group': group_name,
                                'group_value': group_value
                            }

                            # Extraer texto de cada celda
                            for cell_idx, cell in enumerate(cells):
                                try:
                                    cell_text = cell.inner_text().strip()
                                    food_data[f'column_{cell_idx}'] = cell_text
                                except:
                                    food_data[f'column_{cell_idx}'] = ''

                            group_foods.append(food_data)

                            # Mostrar primeras 3 columnas
                            preview = ' | '.join([
                                food_data.get('column_0', ''),
                                food_data.get('column_1', ''),
                                food_data.get('column_2', '')
                            ])
                            print(f"  ✅ Fila {row_idx}: {preview[:80]}")

                        except Exception as e:
                            print(f"  ❌ Error en fila {row_idx}: {e}")
                            continue

                    all_foods_by_group[group_name] = group_foods
                    print(f"\n✅ Extraídos {len(group_foods)} alimentos del grupo '{group_name}'")

                except Exception as e:
                    print(f"❌ Error procesando grupo {group_name}: {e}")
                    import traceback
                    traceback.print_exc()
                    continue

        except Exception as e:
            print(f"\n❌ Error durante el scraping: {e}")
            import traceback
            traceback.print_exc()

            # Screenshot de error
            try:
                page.screenshot(path="screenshot_error.png")
                print("📸 Screenshot de error: screenshot_error.png")
            except:
                pass

        finally:
            print("\n🔒 Cerrando navegador...")
            input("\n⏸️ Presiona ENTER para cerrar el navegador y continuar...")
            browser.close()

    return all_foods_by_group


def save_to_json(foods_by_group, output_file='smae_foods_all_groups.json'):
    """Guardar todos los alimentos a JSON"""

    output_path = Path(__file__).parent.parent / 'data' / output_file

    print(f"\n💾 Guardando datos en {output_path}...")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(foods_by_group, f, ensure_ascii=False, indent=2)

    total_foods = sum(len(foods) for foods in foods_by_group.values())
    print(f"✅ Guardados {total_foods} alimentos de {len(foods_by_group)} grupos")


def save_to_database(foods_by_group):
    """Guardar alimentos en la base de datos"""

    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL no está configurada")
        return

    # Convertir async driver a sync driver
    database_url = database_url.replace('postgresql+asyncpg', 'postgresql')

    print("\n🗄️ Conectando a base de datos...")
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()

    try:
        foods_added = 0
        foods_skipped = 0

        for group_name, foods in foods_by_group.items():
            print(f"\n📦 Procesando grupo: {group_name}")

            for food_data in foods:
                try:
                    # Extraer nombre (asumiendo que está en column_0 o column_1)
                    name = food_data.get('column_0', '') or food_data.get('column_1', '')

                    if not name or len(name) < 2:
                        continue

                    # Verificar si ya existe
                    cursor.execute("SELECT id FROM foods WHERE name = %s", (name,))
                    if cursor.fetchone():
                        foods_skipped += 1
                        continue

                    # Mapear categoría
                    category = CATEGORY_MAP.get(group_name.lower(), 'CEREALS')

                    # Insertar alimento básico
                    # (necesitarás ajustar esto según la estructura real de la tabla)
                    insert_query = """
                    INSERT INTO foods (
                        name, category, subcategory, base_unit, serving_size,
                        calories_per_serving, protein_g, carbs_g, fat_g,
                        source, status, created_at
                    ) VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, NOW()
                    )
                    """

                    cursor.execute(insert_query, (
                        name,
                        category,
                        group_name,
                        'GRAMS',
                        100.0,
                        0.0,  # calories
                        0.0,  # protein
                        0.0,  # carbs
                        0.0,  # fat
                        'SMAE - Sistema Mexicano de Alimentos Equivalentes',
                        'APPROVED'
                    ))

                    foods_added += 1
                    print(f"  ✅ {name}")

                except Exception as e:
                    print(f"  ❌ Error: {name} - {e}")
                    continue

        conn.commit()

        print(f"\n{'='*60}")
        print(f"✅ Proceso completado!")
        print(f"   Alimentos agregados: {foods_added}")
        print(f"   Alimentos omitidos: {foods_skipped}")
        print(f"{'='*60}")

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    try:
        # Scrape todos los grupos
        print("🚀 Iniciando scraping de todos los grupos SMAE...")
        foods_by_group = scrape_all_groups()

        if foods_by_group:
            # Guardar a JSON
            save_to_json(foods_by_group)

            # Preguntar si quiere guardar en BD
            response = input("\n¿Deseas guardar los alimentos en la base de datos? (s/n): ")
            if response.lower() == 's':
                save_to_database(foods_by_group)

            print("\n" + "="*60)
            print("✅ Scraping completado exitosamente!")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("⚠️ No se extrajeron alimentos")
            print("Revisa los screenshots generados")
            print("="*60)
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ ERROR FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
