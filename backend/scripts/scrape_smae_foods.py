"""
Script para scrape alimentos del sistema SMAE desde la web oficial
https://midietasmae.com.mx/Manager/Grupo/Default.aspx

Requiere Playwright instalado: pip install playwright && playwright install chromium
"""
import sys
import os
import json
import time
import re
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Credenciales de acceso
LOGIN_URL = "https://midietasmae.com.mx/Manager/Grupo/Default.aspx"
EMAIL = "ajcortest@gmail.com"
PASSWORD = "Lisa01183116"

# Mapeo de categorías SMAE a categorías del sistema
CATEGORY_MAP = {
    'cereales_sin_grasa': 'cereals',
    'cereales_con_grasa': 'cereals',
    'leguminosas': 'legumes',
    'verduras': 'vegetables',
    'frutas': 'fruits',
    'leche_descremada': 'dairy',
    'leche_semidescremada': 'dairy',
    'leche_entera': 'dairy',
    'carnes_muy_bajo_aporte': 'animal_products',
    'carnes_bajo_aporte': 'animal_products',
    'carnes_moderado_aporte': 'animal_products',
    'carnes_alto_aporte': 'animal_products',
    'grasas_sin_proteina': 'fats',
    'grasas_con_proteina': 'fats',
    'azucares_sin_grasa': 'sugars',
    'azucares_con_grasa': 'sugars',
    'bebida_libre': 'beverages'
}


def scrape_smae_foods():
    """Scrape alimentos desde el sitio web oficial de SMAE"""

    print("🌐 Iniciando scraping de alimentos SMAE...")
    print(f"URL: {LOGIN_URL}")

    all_foods = []

    with sync_playwright() as p:
        # Lanzar navegador
        print("\n🚀 Lanzando navegador Chromium...")
        browser = p.chromium.launch(
            headless=False,  # Mostrar navegador para debugging
            slow_mo=500  # Slow down para poder ver qué pasa
        )

        # Crear contexto y página
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()

        try:
            # Navegar a la página de login
            print(f"\n📍 Navegando a {LOGIN_URL}...")
            page.goto(LOGIN_URL, wait_until='networkidle', timeout=30000)

            # Esperar a que cargue la página
            time.sleep(2)

            print("\n🔍 Buscando formulario de login...")

            # Tomar screenshot del estado inicial
            page.screenshot(path="screenshot_login_page.png")
            print("📸 Screenshot guardado: screenshot_login_page.png")

            # Buscar campos de login (ASP.NET usa IDs específicos)
            # Intentar varios selectores comunes para ASP.NET
            email_selectors = [
                'input[type="email"]',
                'input[id*="Email"]',
                'input[id*="email"]',
                'input[id*="Usuario"]',
                'input[id*="UserName"]',
                'input[name*="email"]',
                'input[name*="Email"]',
            ]

            password_selectors = [
                'input[type="password"]',
                'input[id*="Password"]',
                'input[id*="password"]',
                'input[id*="Contraseña"]',
                'input[name*="password"]',
                'input[name*="Password"]',
            ]

            # Intentar encontrar campos de email
            email_field = None
            for selector in email_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        email_field = selector
                        print(f"✅ Campo de email encontrado: {selector}")
                        break
                except:
                    continue

            # Intentar encontrar campos de password
            password_field = None
            for selector in password_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        password_field = selector
                        print(f"✅ Campo de password encontrado: {selector}")
                        break
                except:
                    continue

            if not email_field or not password_field:
                # Obtener el HTML de la página para analizar
                html = page.content()

                # Guardar HTML para análisis
                with open('login_page.html', 'w', encoding='utf-8') as f:
                    f.write(html)
                print("📄 HTML guardado en: login_page.html")

                # Buscar todos los inputs
                inputs = page.locator('input').all()
                print(f"\n🔍 Encontrados {len(inputs)} campos input:")
                for i, inp in enumerate(inputs):
                    try:
                        input_type = inp.get_attribute('type') or 'text'
                        input_id = inp.get_attribute('id') or 'N/A'
                        input_name = inp.get_attribute('name') or 'N/A'
                        print(f"  {i+1}. Type: {input_type}, ID: {input_id}, Name: {input_name}")
                    except:
                        pass

                print("\n❌ No se pudieron encontrar los campos de login")
                print("Por favor revisa login_page.html y screenshot_login_page.png")
                return []

            # Llenar formulario
            print(f"\n📝 Llenando formulario de login...")
            page.fill(email_field, EMAIL)
            print(f"  ✅ Email ingresado: {EMAIL}")

            page.fill(password_field, PASSWORD)
            print(f"  ✅ Password ingresado")

            # Buscar botón de submit
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Iniciar")',
                'button:has-text("Entrar")',
                'button:has-text("Login")',
                'input[value*="Iniciar"]',
                'input[value*="Entrar"]',
            ]

            submit_button = None
            for selector in submit_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        submit_button = selector
                        print(f"✅ Botón de submit encontrado: {selector}")
                        break
                except:
                    continue

            if not submit_button:
                print("❌ No se encontró botón de submit")
                # Buscar todos los botones
                buttons = page.locator('button, input[type="submit"], input[type="button"]').all()
                print(f"\n🔍 Encontrados {len(buttons)} botones:")
                for i, btn in enumerate(buttons):
                    try:
                        btn_text = btn.inner_text() or btn.get_attribute('value') or 'N/A'
                        btn_id = btn.get_attribute('id') or 'N/A'
                        print(f"  {i+1}. Text/Value: {btn_text}, ID: {btn_id}")
                    except:
                        pass
                return []

            # Hacer click en submit
            print("\n🔐 Intentando login...")
            page.click(submit_button)

            # Esperar navegación
            try:
                page.wait_for_load_state('networkidle', timeout=10000)
                time.sleep(2)
            except PlaywrightTimeoutError:
                print("⏱️ Timeout esperando navegación, continuando...")

            # Verificar si el login fue exitoso
            current_url = page.url
            print(f"\n📍 URL actual: {current_url}")

            # Tomar screenshot después del login
            page.screenshot(path="screenshot_after_login.png")
            print("📸 Screenshot guardado: screenshot_after_login.png")

            # Si la URL cambió o hay ciertos elementos, el login fue exitoso
            if current_url != LOGIN_URL or page.locator('text=Cerrar sesión').count() > 0:
                print("✅ Login exitoso!")
            else:
                # Verificar si hay mensajes de error
                error_selectors = [
                    '.error',
                    '.alert',
                    '[class*="error"]',
                    '[class*="alert"]',
                    'text=/error/i',
                    'text=/incorrecto/i'
                ]

                for selector in error_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            error_text = page.locator(selector).first.inner_text()
                            print(f"❌ Error de login: {error_text}")
                            return []
                    except:
                        pass

                print("⚠️ No se puede confirmar si el login fue exitoso")

            # Ahora intentar extraer los alimentos
            print("\n🍎 Extrayendo alimentos del sistema...")

            # Buscar tabla de alimentos o grupos
            # ASP.NET suele usar GridView con IDs específicos
            table_selectors = [
                'table[id*="Grid"]',
                'table[id*="grid"]',
                'table.table',
                'table',
                '[id*="GridView"]',
            ]

            table_found = None
            for selector in table_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        table_found = selector
                        print(f"✅ Tabla encontrada: {selector}")
                        break
                except:
                    continue

            if not table_found:
                print("❌ No se encontró tabla de alimentos")
                # Guardar HTML de la página actual
                with open('dashboard_page.html', 'w', encoding='utf-8') as f:
                    f.write(page.content())
                print("📄 HTML guardado en: dashboard_page.html")
                return []

            # Extraer filas de la tabla
            rows = page.locator(f'{table_found} tr').all()
            print(f"📊 Encontradas {len(rows)} filas en la tabla")

            # Procesar cada fila
            for i, row in enumerate(rows[1:], 1):  # Skip header row
                try:
                    cells = row.locator('td').all()
                    if len(cells) < 2:
                        continue

                    # Extraer datos de las celdas
                    # La estructura dependerá de cómo está organizada la tabla
                    food_data = {
                        'row_index': i,
                        'cells': []
                    }

                    for cell in cells:
                        try:
                            food_data['cells'].append(cell.inner_text())
                        except:
                            food_data['cells'].append('')

                    all_foods.append(food_data)
                    print(f"  ✅ Fila {i}: {' | '.join(food_data['cells'][:3])}")

                except Exception as e:
                    print(f"  ❌ Error procesando fila {i}: {e}")
                    continue

            print(f"\n✅ Se extrajeron {len(all_foods)} alimentos")

        except Exception as e:
            print(f"\n❌ Error durante el scraping: {e}")
            import traceback
            traceback.print_exc()

            # Tomar screenshot del error
            try:
                page.screenshot(path="screenshot_error.png")
                print("📸 Screenshot de error guardado: screenshot_error.png")
            except:
                pass

        finally:
            # Cerrar navegador
            print("\n🔒 Cerrando navegador...")
            browser.close()

    return all_foods


def save_foods_to_json(foods, output_file='smae_foods_scraped.json'):
    """Guardar alimentos extraídos a un archivo JSON"""

    output_path = Path(__file__).parent.parent / 'data' / output_file

    print(f"\n💾 Guardando {len(foods)} alimentos en {output_path}...")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(foods, f, ensure_ascii=False, indent=2)

    print(f"✅ Alimentos guardados en {output_path}")
    print(f"📊 Total de alimentos: {len(foods)}")


if __name__ == "__main__":
    try:
        # Scrape alimentos
        foods = scrape_smae_foods()

        if foods:
            # Guardar a JSON
            save_foods_to_json(foods)

            print("\n" + "="*60)
            print("✅ Scraping completado exitosamente!")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("⚠️ No se extrajeron alimentos")
            print("Revisa los screenshots y archivos HTML generados")
            print("="*60)
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ ERROR FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
