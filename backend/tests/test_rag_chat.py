"""
Test RAG Chat Endpoint with Gemini AI
======================================

Script para probar el endpoint de chat RAG con Gemini AI.
"""

import asyncio
import httpx
import json
from datetime import datetime


BASE_URL = "http://localhost:8000/api/v1"


async def test_rag_chat():
    """
    Prueba el endpoint /rag/chat con Gemini AI
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("=" * 80)
        print("🧪 TEST: RAG Chat con Gemini AI")
        print("=" * 80)
        print()

        # Paso 1: Registrar usuario de prueba
        print("📝 Paso 1: Registrando usuario de prueba...")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        test_user = {
            "email": f"rag_test_{timestamp}@test.com",
            "username": f"ragtest{timestamp}",
            "password": "Test123456",
            "confirm_password": "Test123456",
            "first_name": "RAG",
            "last_name": "Test",
            "phone": "+52 55 1234 5678",
            "role": "nutritionist"
        }

        try:
            register_response = await client.post(
                f"{BASE_URL}/auth/register",
                json=test_user
            )

            if register_response.status_code == 201:
                print(f"   ✅ Usuario registrado: {test_user['email']}")
                user_data = register_response.json()
            elif register_response.status_code == 400:
                print(f"   ℹ️  Usuario ya existe, intentando login...")
                # Si el usuario ya existe, intentar login
                login_response = await client.post(
                    f"{BASE_URL}/auth/login",
                    data={
                        "username": test_user["username"],
                        "password": test_user["password"]
                    }
                )
                if login_response.status_code == 200:
                    user_data = login_response.json()
                    print(f"   ✅ Login exitoso")
                else:
                    print(f"   ❌ Error en login: {login_response.status_code}")
                    print(f"   {login_response.text}")
                    return
            else:
                print(f"   ❌ Error en registro: {register_response.status_code}")
                print(f"   {register_response.text}")
                return

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return

        print()

        # Paso 2: Obtener token de acceso
        print("🔑 Paso 2: Obteniendo token de acceso...")
        try:
            if "access_token" in user_data:
                access_token = user_data["access_token"]
                print(f"   ✅ Token obtenido: {access_token[:20]}...")
            else:
                print(f"   ❌ No se encontró access_token en respuesta")
                return
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return

        print()

        # Paso 3: Probar endpoint /rag/chat
        print("🤖 Paso 3: Probando endpoint /rag/chat con Gemini AI...")
        print()

        test_messages = [
            {
                "message": "¿Qué alimentos son buenos para bajar el colesterol?",
                "include_context": False,
                "include_search_results": False
            },
            {
                "message": "¿Cuántas calorías tiene una tortilla de maíz?",
                "include_context": False,
                "include_search_results": True
            },
            {
                "message": "Dame un plan de alimentación saludable para una persona con diabetes",
                "include_context": True,
                "include_search_results": True
            }
        ]

        for i, test_msg in enumerate(test_messages, 1):
            print(f"   📨 Test {i}/3: {test_msg['message'][:60]}...")
            print(f"      Context: {test_msg['include_context']}, Search: {test_msg['include_search_results']}")

            try:
                chat_response = await client.post(
                    f"{BASE_URL}/rag/chat",
                    json=test_msg,
                    headers={"Authorization": f"Bearer {access_token}"}
                )

                if chat_response.status_code == 200:
                    chat_data = chat_response.json()

                    print(f"      ✅ Respuesta exitosa ({chat_response.status_code})")
                    print()
                    print(f"      📊 Modelo: {chat_data.get('model', 'N/A')}")
                    print(f"      📊 Contexto incluido: {chat_data.get('context_included', False)}")
                    print(f"      📊 Búsqueda incluida: {chat_data.get('search_included', False)}")

                    if chat_data.get('usage'):
                        usage = chat_data['usage']
                        print(f"      📊 Tokens:")
                        print(f"         - Prompt: {usage.get('prompt_tokens', 0)}")
                        print(f"         - Completion: {usage.get('completion_tokens', 0)}")
                        print(f"         - Total: {usage.get('total_tokens', 0)}")

                    print()
                    print("      💬 Respuesta de Gemini AI:")
                    print("      " + "-" * 70)
                    ai_response = chat_data.get('ai_response', 'No response')
                    # Mostrar solo las primeras 500 caracteres
                    if len(ai_response) > 500:
                        print(f"      {ai_response[:500]}...")
                        print(f"      ... ({len(ai_response)} caracteres totales)")
                    else:
                        print(f"      {ai_response}")
                    print("      " + "-" * 70)
                    print()
                else:
                    print(f"      ❌ Error: {chat_response.status_code}")
                    print(f"      {chat_response.text}")
                    print()

            except Exception as e:
                print(f"      ❌ Error en request: {str(e)}")
                print()

            # Pequeña pausa entre requests
            await asyncio.sleep(1)

        print()
        print("=" * 80)
        print("✅ TEST COMPLETADO")
        print("=" * 80)


async def test_rag_health():
    """
    Prueba el endpoint de health check del RAG
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        print("=" * 80)
        print("🏥 TEST: RAG Health Check")
        print("=" * 80)
        print()

        try:
            response = await client.get(f"{BASE_URL}/rag/health")

            if response.status_code == 200:
                data = response.json()
                print("✅ RAG Service Status:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)

        except Exception as e:
            print(f"❌ Error: {str(e)}")

        print()


async def main():
    """
    Ejecuta todos los tests
    """
    print()
    print("🚀 Iniciando tests del sistema RAG con Gemini AI")
    print()

    # Test 1: Health check
    await test_rag_health()

    print()

    # Test 2: Chat con Gemini AI
    await test_rag_chat()


if __name__ == "__main__":
    asyncio.run(main())
