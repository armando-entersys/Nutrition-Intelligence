"""
============================================================================
Script de Limpieza de Base de Datos - Producción
============================================================================
Este script elimina TODOS los datos de desarrollo/prueba
y deja ÚNICAMENTE los catálogos esenciales:
- Alimentos SMAE
- Recetas

ADVERTENCIA: Esta acción es IRREVERSIBLE
Use solo para preparar el sistema para producción
============================================================================
"""

import sys
import os
from pathlib import Path

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Agregar el directorio padre al path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import asyncio


def cleanup_database(skip_confirmation=False):
    """
    Limpia la base de datos eliminando datos de desarrollo
    y manteniendo solo catálogos esenciales
    """

    # Conectar a la base de datos
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./nutrition_intelligence.db")

    # Para SQLite async, usar sync version para este script
    if "sqlite+aiosqlite" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("sqlite+aiosqlite", "sqlite")
    elif "postgresql+asyncpg" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg", "postgresql")

    engine = create_engine(DATABASE_URL, echo=True)

    print("\n" + "="*80)
    print("🚨 LIMPIEZA DE BASE DE DATOS - PRODUCCIÓN")
    print("="*80)
    print()
    print("Este script eliminará:")
    print("  ❌ Todos los pacientes")
    print("  ❌ Todos los expedientes clínicos")
    print("  ❌ Todos los datos de laboratorio")
    print("  ❌ Todos los archivos clínicos")
    print("  ❌ Todos los mensajes WhatsApp")
    print("  ❌ Todos los planes de alimentación")
    print("  ❌ Todos los usuarios de prueba")
    print()
    print("Mantendrá:")
    print("  ✅ Catálogo de Alimentos SMAE")
    print("  ✅ Catálogo de Recetas")
    print()
    print("="*80)

    if not skip_confirmation:
        respuesta = input("\n¿Estás SEGURO de que quieres continuar? (escribe 'SÍ ELIMINAR' para confirmar): ")

        if respuesta != "SÍ ELIMINAR":
            print("\n❌ Operación cancelada por el usuario")
            return
    else:
        print("\n⚠️  Modo automático: saltando confirmación")

    print("\n🔄 Iniciando limpieza...")

    with Session(engine) as session:
        try:
            # ELIMINAR en orden (respetando foreign keys)
            # Usar try-except para cada tabla por si no existe

            def safe_delete(table_name, description):
                """Elimina datos de una tabla si existe"""
                try:
                    print(f"\n🗑️  Eliminando {description}...")
                    result = session.execute(text(f"DELETE FROM {table_name}"))
                    print(f"   ✅ {result.rowcount} registros eliminados")
                except Exception as e:
                    if "no such table" in str(e):
                        print(f"   ⚠️  Tabla '{table_name}' no existe (saltando)")
                    else:
                        raise

            # 1. Mensajes WhatsApp
            safe_delete("whatsapp_messages", "mensajes WhatsApp")

            # 2. Archivos clínicos
            safe_delete("clinical_files", "archivos clínicos")

            # 3. Datos de laboratorio
            safe_delete("laboratory_data", "datos de laboratorio")

            # 4. Planes de alimentación
            safe_delete("meal_plans", "planes de alimentación")

            # 5. Mediciones antropométricas
            safe_delete("anthropometric_measurements", "mediciones antropométricas")

            # 6. Signos vitales
            safe_delete("vital_signs", "signos vitales")

            # 7. Historia clínica
            safe_delete("clinical_history", "historia clínica")

            # 8. Pacientes
            safe_delete("patients", "pacientes")

            # 9. Usuarios (EXCEPTO admin si existe)
            try:
                print("\n🗑️  Eliminando usuarios de prueba...")
                result = session.execute(text("DELETE FROM users WHERE email NOT LIKE '%admin%'"))
                print(f"   ✅ {result.rowcount} usuarios eliminados")
            except Exception as e:
                if "no such table" in str(e):
                    print(f"   ⚠️  Tabla 'users' no existe (saltando)")
                else:
                    raise

            # 10. Logs y auditoría (opcional - comentar si se quiere mantener)
            # safe_delete("audit_logs", "logs de auditoría")

            # COMMIT de todos los cambios
            session.commit()

            print("\n" + "="*80)
            print("✅ LIMPIEZA COMPLETADA EXITOSAMENTE")
            print("="*80)

            # Mostrar qué datos permanecen
            print("\n📊 Datos que permanecen en la base de datos:")

            # Contar alimentos
            result = session.execute(text("SELECT COUNT(*) FROM foods"))
            foods_count = result.scalar()
            print(f"   🥗 Alimentos SMAE: {foods_count}")

            # Contar recetas
            result = session.execute(text("SELECT COUNT(*) FROM recipes"))
            recipes_count = result.scalar()
            print(f"   📖 Recetas: {recipes_count}")

            # Contar usuarios restantes
            result = session.execute(text("SELECT COUNT(*) FROM users"))
            users_count = result.scalar()
            print(f"   👤 Usuarios: {users_count} (solo admin)")

            print("\n✨ La base de datos está lista para producción!")
            print()

        except Exception as e:
            session.rollback()
            print(f"\n❌ ERROR durante la limpieza: {str(e)}")
            raise


def create_production_users():
    """
    Crea los 2 usuarios de producción:
    1. Nutriólogo profesional
    2. Cliente/Paciente
    """

    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./nutrition_intelligence.db")

    if "sqlite+aiosqlite" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("sqlite+aiosqlite", "sqlite")
    elif "postgresql+asyncpg" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg", "postgresql")

    engine = create_engine(DATABASE_URL, echo=False)

    print("\n" + "="*80)
    print("👥 CREACIÓN DE USUARIOS DE PRODUCCIÓN")
    print("="*80)

    with Session(engine) as session:
        try:
            from passlib.context import CryptContext
            from datetime import datetime

            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

            # 1. Crear Nutriólogo
            print("\n1️⃣  Creando usuario: Nutriólogo Profesional")

            hashed_password_nutri = pwd_context.hash("nutriologo123")

            session.execute(text("""
                INSERT INTO users (
                    email,
                    hashed_password,
                    first_name,
                    last_name,
                    role,
                    status,
                    created_at,
                    updated_at,
                    email_verified,
                    phone_verified
                ) VALUES (
                    :email,
                    :password,
                    :first_name,
                    :last_name,
                    :role,
                    :status,
                    :created,
                    :updated,
                    :email_verified,
                    :phone_verified
                )
            """), {
                "email": "nutriologo@nutrition-intelligence.com",
                "password": hashed_password_nutri,
                "first_name": "Ana María",
                "last_name": "Pérez Lizaur",
                "role": "nutritionist",
                "status": "active",
                "created": datetime.utcnow(),
                "updated": datetime.utcnow(),
                "email_verified": True,
                "phone_verified": False
            })

            print("   ✅ Nutriólogo creado:")
            print("      📧 Email: nutriologo@nutrition-intelligence.com")
            print("      🔑 Password: nutriologo123")
            print("      👤 Nombre: Dra. Ana María Pérez Lizaur")
            print("      🏥 Rol: Nutriólogo")

            # 2. Crear Paciente
            print("\n2️⃣  Creando usuario: Cliente/Paciente")

            hashed_password_patient = pwd_context.hash("cliente123")

            session.execute(text("""
                INSERT INTO users (
                    email,
                    hashed_password,
                    first_name,
                    last_name,
                    role,
                    status,
                    created_at,
                    updated_at,
                    email_verified,
                    phone_verified
                ) VALUES (
                    :email,
                    :password,
                    :first_name,
                    :last_name,
                    :role,
                    :status,
                    :created,
                    :updated,
                    :email_verified,
                    :phone_verified
                )
            """), {
                "email": "cliente@nutrition-intelligence.com",
                "password": hashed_password_patient,
                "first_name": "María Guadalupe",
                "last_name": "Hernández López",
                "role": "patient",
                "status": "active",
                "created": datetime.utcnow(),
                "updated": datetime.utcnow(),
                "email_verified": True,
                "phone_verified": False
            })

            print("   ✅ Cliente creado:")
            print("      📧 Email: cliente@nutrition-intelligence.com")
            print("      🔑 Password: cliente123")
            print("      👤 Nombre: María Guadalupe Hernández López")
            print("      🧑 Rol: Paciente")

            session.commit()

            print("\n" + "="*80)
            print("✅ USUARIOS DE PRODUCCIÓN CREADOS")
            print("="*80)
            print()

        except Exception as e:
            session.rollback()
            print(f"\n❌ ERROR creando usuarios: {str(e)}")
            raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Limpieza de base de datos para producción")
    parser.add_argument("--cleanup", action="store_true", help="Limpiar base de datos")
    parser.add_argument("--create-users", action="store_true", help="Crear usuarios de producción")
    parser.add_argument("--all", action="store_true", help="Ejecutar limpieza completa + crear usuarios")
    parser.add_argument("--yes", action="store_true", help="Saltar confirmación (modo automático)")

    args = parser.parse_args()

    if args.all:
        cleanup_database(skip_confirmation=args.yes)
        create_production_users()
    elif args.cleanup:
        cleanup_database(skip_confirmation=args.yes)
    elif args.create_users:
        create_production_users()
    else:
        print("Uso:")
        print("  python cleanup_database.py --cleanup         # Solo limpiar BD")
        print("  python cleanup_database.py --create-users    # Solo crear usuarios")
        print("  python cleanup_database.py --all             # Limpieza completa + usuarios")
        print("  python cleanup_database.py --all --yes       # Modo automático sin confirmación")
