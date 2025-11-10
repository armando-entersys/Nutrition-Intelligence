"""
Script completo para scraping de SMAE
Login -> Selección de grupos -> Paginación -> CSV Export

Flujo:
1. Login en https://midietasmae.com.mx/Login/
2. Navegar a https://midietasmae.com.mx/Manager/Grupo/Default.aspx
3. Para cada grupo:
   - Seleccionar grupo del dropdown
   - Configurar para mostrar 100 registros
   - Navegar por todas las hojas/páginas
   - Extraer TODOS los alimentos
4. Guardar en CSV para importar a BD
"""
import sys
import os
import csv
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# URLs y credenciales
LOGIN_URL = "https://midietasmae.com.mx/Login/"
MANAGER_URL = "https://midietasmae.com.mx/Manager/Grupo/Default.aspx"
EMAIL = "ajcortest@gmail.com"
PASSWORD = "Lisa01183116"

def scrape_smae_complete():
    """Scraping completo de SMAE con login y paginación"""

    print("🌐 Iniciando scraping completo de SMAE...")
    print(f"Login URL: {LOGIN_URL}")
    print(f"Manager URL: {MANAGER_URL}")

    all_foods = []

    with sync_playwright() as p:
        # Lanzar navegador
        print("\n🚀 Lanzando navegador Chromium...")
        browser = p.chromium.launch(
            headless=False,  # Visible para debugging
            slow_mo=500  # Slower para ver el proceso
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
            print(f"\n{'='*60}")
            print("PASO 1: LOGIN")
            print(f"{'='*60}")

            print(f"📍 Navegando a {LOGIN_URL}...")
            page.goto(LOGIN_URL, wait_until='networkidle', timeout=30000)
            time.sleep(2)

            # Screenshot inicial
            page.screenshot(path="01_login_page.png")
            print("📸 Screenshot: 01_login_page.png")

            # Buscar campos de login
            print("\n🔍 Buscando campos de login...")

            email_input = None
            password_input = None

            # Intentar encontrar inputs por tipo y atributos comunes
            inputs = page.locator('input').all()

            for inp in inputs:
                try:
                    input_type = inp.get_attribute('type') or ''
                    input_id = inp.get_attribute('id') or ''
                    input_name = inp.get_attribute('name') or ''

                    # Campo de email/usuario
                    if input_type == 'email' or 'email' in input_id.lower() or 'email' in input_name.lower():
                        email_input = inp
                        print(f"✅ Email input: {input_id or input_name}")

                    # Campo de password
                    if input_type == 'password':
                        password_input = inp
                        print(f"✅ Password input: {input_id or input_name}")

                except:
                    continue

            if not email_input or not password_input:
                print("❌ No se encontraron campos de login")
                return []

            # Llenar formulario
            print(f"\n📝 Llenando formulario...")
            email_input.fill(EMAIL)
            print(f"  Email: {EMAIL}")

            password_input.fill(PASSWORD)
            print(f"  Password: ****")

            # Buscar botón de submit
            submit_button = page.locator('button[type="submit"], input[type="submit"]').first

            # Screenshot antes de submit
            page.screenshot(path="02_before_submit.png")
            print("📸 Screenshot: 02_before_submit.png")

            # Hacer login - intentar múltiples métodos
            print("\n🔐 Haciendo login...")

            login_successful = False

            # Método 1: Click con force=True (bypass visibility check)
            try:
                print("  Intentando click con force=True...")
                submit_button.click(force=True, timeout=5000)
                login_successful = True
                print("  ✅ Click exitoso con force=True")
            except Exception as e:
                print(f"  ⚠️ Click con force=True falló: {e}")

            # Método 2: JavaScript click
            if not login_successful:
                try:
                    print("  Intentando click con JavaScript...")
                    page.evaluate("""
                        const submitBtn = document.querySelector('button[type="submit"], input[type="submit"]');
                        if (submitBtn) submitBtn.click();
                    """)
                    login_successful = True
                    print("  ✅ Click exitoso con JavaScript")
                except Exception as e:
                    print(f"  ⚠️ Click con JavaScript falló: {e}")

            # Método 3: Submit del formulario directamente
            if not login_successful:
                try:
                    print("  Intentando submit del formulario...")
                    page.evaluate("""
                        const form = document.querySelector('form');
                        if (form) form.submit();
                    """)
                    login_successful = True
                    print("  ✅ Submit del formulario exitoso")
                except Exception as e:
                    print(f"  ⚠️ Submit del formulario falló: {e}")

            # Método 4: Presionar Enter en el campo de password
            if not login_successful:
                try:
                    print("  Intentando presionar Enter en el campo de password...")
                    password_input.press('Enter')
                    login_successful = True
                    print("  ✅ Enter presionado exitosamente")
                except Exception as e:
                    print(f"  ⚠️ Presionar Enter falló: {e}")

            if not login_successful:
                print("❌ Todos los métodos de login fallaron")
                return []

            # Esperar navegación
            try:
                page.wait_for_load_state('networkidle', timeout=10000)
            except:
                print("⏱️ Timeout esperando navegación, continuando...")
                pass

            time.sleep(3)

            # Verificar login exitoso
            current_url = page.url
            print(f"📍 URL después de login: {current_url}")

            page.screenshot(path="03_after_login.png")
            print("📸 Screenshot: 03_after_login.png")

            # Guardar HTML para debugging
            with open('03_after_login.html', 'w', encoding='utf-8') as f:
                f.write(page.content())
            print("📄 HTML guardado: 03_after_login.html")

            # Verificar si hay errores de login
            error_indicators = [
                'incorrecto', 'error', 'inválido', 'credenciales',
                'usuario o contraseña', 'login failed'
            ]
            page_content = page.content().lower()
            for indicator in error_indicators:
                if indicator in page_content:
                    print(f"❌ Posible error de login detectado: '{indicator}' encontrado en la página")
                    print("Verifica las credenciales o revisa el archivo 03_after_login.html")
                    return []

            # Verificar si seguimos en la página de login
            if 'login' in current_url.lower() and '/login/' in current_url:
                print("⚠️ Advertencia: Aún en la página de login después del submit")
                print("Esto podría indicar credenciales incorrectas o validación de JavaScript")
                # Intentar continuar de todos modos
            else:
                print("✅ Login parece exitoso (URL cambió)")

            # Esperar un poco más después del login
            time.sleep(2)

            # ============================================
            # PASO 2: NAVEGAR A MANAGER
            # ============================================
            print(f"\n{'='*60}")
            print("PASO 2: NAVEGAR A MANAGER")
            print(f"{'='*60}")

            print(f"📍 Navegando a {MANAGER_URL}...")
            page.goto(MANAGER_URL, wait_until='networkidle', timeout=30000)
            time.sleep(2)

            page.screenshot(path="04_manager_page.png")
            print("📸 Screenshot: 04_manager_page.png")

            # ============================================
            # PASO 3: ENCONTRAR DROPDOWN DE GRUPOS
            # ============================================
            print(f"\n{'='*60}")
            print("PASO 3: ENCONTRAR DROPDOWN DE GRUPOS")
            print(f"{'='*60}")

            # Buscar el select de grupos
            selects = page.locator('select').all()
            print(f"📋 Encontrados {len(selects)} elementos select")

            group_select = None
            if len(selects) > 0:
                group_select = selects[0]  # Usar el primer select
                print(f"✅ Usando el primer select como dropdown de grupos")
            else:
                print("❌ No se encontró dropdown de grupos")
                return []

            # Obtener todas las opciones
            options = group_select.locator('option').all()
            print(f"📋 Encontradas {len(options)} opciones")

            group_options = []
            for i, opt in enumerate(options):
                try:
                    value = opt.get_attribute('value') or ''
                    text = opt.inner_text() or ''

                    # Saltar opciones vacías
                    if value and value != '0' and 'seleccione' not in text.lower():
                        group_options.append({'value': value, 'text': text})
                        print(f"  {i}. {text} (value={value})")
                except:
                    continue

            print(f"\n✅ Total de grupos a procesar: {len(group_options)}")

            # ============================================
            # PASO 4: PROCESAR CADA GRUPO
            # ============================================
            for group_idx, group in enumerate(group_options, 1):
                group_name = group['text']
                group_value = group['value']

                print(f"\n{'='*60}")
                print(f"GRUPO {group_idx}/{len(group_options)}: {group_name}")
                print(f"{'='*60}")

                try:
                    # Seleccionar grupo
                    print(f"🔄 Seleccionando grupo '{group_name}'...")
                    group_select.select_option(value=group_value)

                    # Esperar a que cargue la tabla
                    time.sleep(3)

                    # Screenshot del grupo
                    page.screenshot(path=f"05_grupo_{group_idx}_{group_name.replace(' ', '_')}.png")

                    # ============================================
                    # CONFIGURAR PARA MOSTRAR 100 REGISTROS
                    # ============================================
                    print("⚙️ Configurando para mostrar 100 registros...")

                    # Buscar el select de "registros por página"
                    # Común en DataTables: select con name que contiene "length"
                    page_size_selects = page.locator('select[name*="length"], select[name*="pageSize"]').all()

                    if len(page_size_selects) > 0:
                        page_size_select = page_size_selects[0]
                        try:
                            page_size_select.select_option(value='100')
                            print("✅ Configurado para mostrar 100 registros")
                            time.sleep(2)
                        except:
                            print("⚠️ No se pudo configurar 100 registros, usando default")
                    else:
                        print("⚠️ No se encontró selector de tamaño de página")

                    # ============================================
                    # EXTRAER DATOS DE TODAS LAS PÁGINAS
                    # ============================================
                    page_num = 1
                    group_foods = []

                    while True:
                        print(f"\n📄 Procesando página {page_num}...")

                        # Buscar tabla
                        tables = page.locator('table').all()

                        if not tables:
                            print("❌ No se encontró tabla")
                            break

                        table = tables[0]

                        # Extraer filas
                        rows = table.locator('tbody tr').all()
                        print(f"📊 Encontradas {len(rows)} filas en página {page_num}")

                        if len(rows) == 0:
                            print("⚠️ No hay más filas, terminando")
                            break

                        # Extraer encabezados (solo en primera página)
                        if page_num == 1:
                            headers = []
                            header_cells = table.locator('thead th').all()
                            for th in header_cells:
                                try:
                                    headers.append(th.inner_text().strip())
                                except:
                                    headers.append('')

                            print(f"📋 Encabezados: {headers}")

                        # Procesar cada fila
                        for row_idx, row in enumerate(rows, 1):
                            try:
                                cells = row.locator('td').all()

                                food_data = {
                                    'grupo': group_name,
                                    'grupo_value': group_value,
                                    'pagina': page_num
                                }

                                # Extraer datos de cada celda
                                for cell_idx, cell in enumerate(cells):
                                    try:
                                        cell_text = cell.inner_text().strip()

                                        # Usar header si está disponible, sino usar índice
                                        if page_num == 1 and cell_idx < len(headers):
                                            col_name = headers[cell_idx]
                                        else:
                                            col_name = f'col_{cell_idx}'

                                        food_data[col_name] = cell_text
                                    except:
                                        food_data[f'col_{cell_idx}'] = ''

                                group_foods.append(food_data)

                                # Mostrar progreso cada 10 filas
                                if row_idx % 10 == 0:
                                    print(f"  ✅ {row_idx} filas procesadas...")

                            except Exception as e:
                                print(f"  ❌ Error en fila {row_idx}: {e}")
                                continue

                        print(f"✅ Página {page_num} completada: {len(rows)} alimentos extraídos")

                        # ============================================
                        # INTENTAR IR A LA SIGUIENTE PÁGINA
                        # ============================================
                        # Buscar botón "Siguiente" o número de página siguiente
                        next_buttons = page.locator('a:has-text("Siguiente"), a:has-text("Next"), .pagination .next:not(.disabled)').all()

                        if len(next_buttons) > 0:
                            try:
                                print(f"🔄 Navegando a página {page_num + 1}...")
                                next_buttons[0].click()
                                time.sleep(2)
                                page_num += 1
                            except:
                                print("⚠️ No se pudo navegar a la siguiente página")
                                break
                        else:
                            # Intentar buscar paginación por números
                            page_links = page.locator(f'.pagination a:has-text("{page_num + 1}")').all()

                            if len(page_links) > 0:
                                try:
                                    print(f"🔄 Navegando a página {page_num + 1}...")
                                    page_links[0].click()
                                    time.sleep(2)
                                    page_num += 1
                                except:
                                    print("⚠️ No hay más páginas")
                                    break
                            else:
                                print("⚠️ No hay más páginas")
                                break

                    # Agregar todos los alimentos del grupo
                    all_foods.extend(group_foods)
                    print(f"\n✅ Grupo '{group_name}' completado: {len(group_foods)} alimentos extraídos")

                except Exception as e:
                    print(f"❌ Error procesando grupo {group_name}: {e}")
                    import traceback
                    traceback.print_exc()
                    continue

        except Exception as e:
            print(f"\n❌ Error durante el scraping: {e}")
            import traceback
            traceback.print_exc()

            try:
                page.screenshot(path="error_screenshot.png")
                print("📸 Screenshot de error: error_screenshot.png")
            except:
                pass

        finally:
            print("\n🔒 Cerrando navegador...")
            browser.close()

    return all_foods


def save_to_csv(foods, output_file='smae_foods_complete.csv'):
    """Guardar alimentos a CSV para importar a BD"""

    if not foods:
        print("⚠️ No hay alimentos para guardar")
        return

    output_path = Path(__file__).parent.parent / 'data' / output_file

    print(f"\n💾 Guardando {len(foods)} alimentos en CSV...")
    print(f"📁 Ruta: {output_path}")

    # Obtener todos los campos únicos
    all_keys = set()
    for food in foods:
        all_keys.update(food.keys())

    # Ordenar campos
    fieldnames = sorted(all_keys)

    # Escribir CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(foods)

    print(f"✅ CSV guardado exitosamente!")
    print(f"📊 Total de alimentos: {len(foods)}")
    print(f"📋 Campos: {len(fieldnames)}")

    # Mostrar estadísticas por grupo
    groups = {}
    for food in foods:
        grupo = food.get('grupo', 'Unknown')
        groups[grupo] = groups.get(grupo, 0) + 1

    print(f"\n📊 Alimentos por grupo:")
    for grupo, count in sorted(groups.items()):
        print(f"  • {grupo}: {count} alimentos")


if __name__ == "__main__":
    try:
        print("🚀 Iniciando scraping completo de SMAE...")
        print("Este proceso puede tomar varios minutos dependiendo de la cantidad de datos")
        print()

        # Scrape todos los alimentos
        foods = scrape_smae_complete()

        if foods:
            # Guardar a CSV
            save_to_csv(foods)

            print("\n" + "="*60)
            print("✅ SCRAPING COMPLETADO EXITOSAMENTE!")
            print("="*60)
            print(f"Total de alimentos extraídos: {len(foods)}")
            print()
            print("Siguiente paso:")
            print("  1. Revisar el archivo CSV generado")
            print("  2. Importar a la base de datos")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("⚠️ NO SE EXTRAJERON ALIMENTOS")
            print("="*60)
            print("Revisa los screenshots generados para identificar el problema")
            print("="*60)
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ ERROR FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
