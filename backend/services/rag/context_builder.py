"""
RAG Context Builder
===================

Construye contexto para el prompt de IA.
Recopila información relevante del usuario para respuestas personalizadas.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from .search_service import RAGSearchService


class RAGContextBuilder:
    """
    Constructor de contexto para RAG

    Recopila y estructura información del usuario para que la IA
    pueda proporcionar respuestas personalizadas y context-aware.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.search_service = RAGSearchService(session)

    async def build_user_context(
        self,
        user_id: int,
        include_scan_history: bool = True,
        include_favorites: bool = True,
        history_days: int = 30,
    ) -> Dict[str, Any]:
        """
        Construir contexto completo del usuario

        Args:
            user_id: ID del usuario
            include_scan_history: Incluir historial de escaneos
            include_favorites: Incluir alimentos favoritos
            history_days: Días de historial a incluir

        Returns:
            Diccionario con contexto del usuario
        """
        context = {
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "scan_history": [],
            "favorite_foods": [],
            "scan_statistics": {},
        }

        # Historial de escaneos
        if include_scan_history:
            scan_history = await self.search_service.get_user_scan_history(
                user_id=user_id,
                limit=100,
            )

            # Filtrar por días
            cutoff_date = datetime.utcnow() - timedelta(days=history_days)
            scan_history = [
                scan for scan in scan_history
                if scan.get("scanned_at") and scan["scanned_at"] >= cutoff_date
            ]

            context["scan_history"] = scan_history
            context["scan_statistics"] = self._calculate_scan_statistics(scan_history)

        # Alimentos favoritos
        if include_favorites:
            favorite_foods = await self.search_service.get_user_favorite_foods(
                user_id=user_id,
            )
            context["favorite_foods"] = favorite_foods

        return context

    async def build_search_context(
        self,
        query: str,
        user_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Construir contexto basado en búsqueda

        Args:
            query: Consulta de búsqueda
            user_id: ID del usuario (opcional)

        Returns:
            Diccionario con resultados de búsqueda
        """
        results = await self.search_service.search_combined(
            query=query,
            user_id=user_id,
            search_products=True,
            search_foods=True,
            limit_per_source=10,
        )

        return {
            "query": query,
            "timestamp": datetime.utcnow().isoformat(),
            "results": results,
        }

    async def build_patient_context(
        self,
        patient_id: int,
        nutritionist_id: int,
    ) -> Dict[str, Any]:
        """
        Construir contexto de paciente (para nutriólogos)

        Args:
            patient_id: ID del paciente
            nutritionist_id: ID del nutriólogo

        Returns:
            Diccionario con contexto del paciente
        """
        # Verificar que el nutriólogo tenga acceso al paciente
        access_query = """
        SELECT 1
        FROM patients
        WHERE id = :patient_id AND nutritionist_id = :nutritionist_id
        """

        result = await self.session.execute(
            access_query,
            {"patient_id": patient_id, "nutritionist_id": nutritionist_id}
        )

        if not result.scalar():
            raise PermissionError(
                f"Nutriólogo {nutritionist_id} no tiene acceso al paciente {patient_id}"
            )

        # Obtener datos del paciente
        patient_query = """
        SELECT
            p.id,
            p.nombre,
            p.apellido,
            p.edad,
            p.sexo,
            p.altura_cm,
            p.peso_kg,
            p.objetivo_nutricional,
            p.restricciones_alimentarias,
            p.alergias,
            p.condiciones_medicas,
            p.nivel_actividad_fisica,
            p.created_at,
            p.updated_at
        FROM patients p
        WHERE p.id = :patient_id
        """

        result = await self.session.execute(
            patient_query,
            {"patient_id": patient_id}
        )

        patient_data = dict(result.mappings().first())

        # Obtener historial de escaneos del paciente
        scan_history = await self.search_service.get_user_scan_history(
            user_id=patient_id,
            limit=100,
        )

        # Obtener alimentos favoritos del paciente
        favorite_foods = await self.search_service.get_user_favorite_foods(
            user_id=patient_id,
        )

        # Obtener planes de comida del paciente
        meal_plans_query = """
        SELECT
            mp.id,
            mp.nombre,
            mp.descripcion,
            mp.fecha_inicio,
            mp.fecha_fin,
            mp.calorias_objetivo,
            mp.proteinas_g_objetivo,
            mp.carbohidratos_g_objetivo,
            mp.grasas_g_objetivo,
            mp.activo
        FROM meal_plans mp
        WHERE mp.patient_id = :patient_id
        ORDER BY mp.created_at DESC
        LIMIT 5
        """

        result = await self.session.execute(
            meal_plans_query,
            {"patient_id": patient_id}
        )

        meal_plans = [dict(row) for row in result.mappings()]

        return {
            "patient": patient_data,
            "scan_history": scan_history,
            "scan_statistics": self._calculate_scan_statistics(scan_history),
            "favorite_foods": favorite_foods,
            "meal_plans": meal_plans,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _calculate_scan_statistics(
        self,
        scan_history: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Calcular estadísticas del historial de escaneos

        Args:
            scan_history: Lista de escaneos

        Returns:
            Diccionario con estadísticas
        """
        if not scan_history:
            return {
                "total_scans": 0,
                "avg_health_score": 0,
                "products_with_seals": 0,
                "most_common_seals": [],
            }

        total_scans = len(scan_history)
        total_health_score = 0
        products_with_seals = 0
        seal_counts = {
            "exceso_calorias": 0,
            "exceso_azucares": 0,
            "exceso_grasas_saturadas": 0,
            "exceso_sodio": 0,
        }

        for scan in scan_history:
            # Health score
            if scan.get("health_score"):
                total_health_score += scan["health_score"]

            # Contar sellos
            has_seals = False
            for seal in seal_counts.keys():
                if scan.get(seal):
                    seal_counts[seal] += 1
                    has_seals = True

            if has_seals:
                products_with_seals += 1

        avg_health_score = total_health_score / total_scans if total_scans > 0 else 0

        # Sellos más comunes
        most_common_seals = sorted(
            seal_counts.items(),
            key=lambda x: x[1],
            reverse=True,
        )[:3]

        return {
            "total_scans": total_scans,
            "avg_health_score": round(avg_health_score, 2),
            "products_with_seals": products_with_seals,
            "products_with_seals_percent": round(
                (products_with_seals / total_scans * 100) if total_scans > 0 else 0,
                2
            ),
            "most_common_seals": [
                {"seal": seal, "count": count}
                for seal, count in most_common_seals
            ],
        }

    def format_context_for_prompt(
        self,
        context: Dict[str, Any],
        max_products: int = 20,
    ) -> str:
        """
        Formatear contexto para incluir en el prompt de IA

        Args:
            context: Diccionario de contexto
            max_products: Máximo de productos a incluir

        Returns:
            String formateado para el prompt
        """
        lines = []

        lines.append("=== CONTEXTO DEL USUARIO ===\n")

        # Estadísticas generales
        if "scan_statistics" in context:
            stats = context["scan_statistics"]
            lines.append(f"Total de escaneos: {stats.get('total_scans', 0)}")
            lines.append(f"Health score promedio: {stats.get('avg_health_score', 0)}")
            lines.append(
                f"Productos con sellos: {stats.get('products_with_seals_percent', 0)}%"
            )

            if stats.get("most_common_seals"):
                lines.append("\nSellos más frecuentes:")
                for seal_data in stats["most_common_seals"]:
                    lines.append(f"  - {seal_data['seal']}: {seal_data['count']} veces")

            lines.append("")

        # Historial reciente
        if "scan_history" in context and context["scan_history"]:
            lines.append(f"\n=== ÚLTIMOS PRODUCTOS ESCANEADOS (máx {max_products}) ===")
            for i, scan in enumerate(context["scan_history"][:max_products]):
                lines.append(
                    f"{i+1}. {scan.get('nombre', 'Sin nombre')} - "
                    f"{scan.get('marca', 'Sin marca')} "
                    f"(Health: {scan.get('health_score', 'N/A')})"
                )
            lines.append("")

        # Alimentos favoritos
        if "favorite_foods" in context and context["favorite_foods"]:
            lines.append("\n=== ALIMENTOS FAVORITOS ===")
            for i, food in enumerate(context["favorite_foods"][:10]):
                lines.append(
                    f"{i+1}. {food.get('nombre_alimento', 'Sin nombre')} "
                    f"({food.get('grupo_alimento', 'Sin grupo')})"
                )
            lines.append("")

        # Datos de paciente (si aplica)
        if "patient" in context:
            patient = context["patient"]
            lines.append("\n=== DATOS DEL PACIENTE ===")
            lines.append(f"Nombre: {patient.get('nombre')} {patient.get('apellido')}")
            lines.append(f"Edad: {patient.get('edad')} años")
            lines.append(f"Sexo: {patient.get('sexo')}")
            lines.append(f"Altura: {patient.get('altura_cm')} cm")
            lines.append(f"Peso: {patient.get('peso_kg')} kg")
            lines.append(f"Objetivo: {patient.get('objetivo_nutricional')}")

            if patient.get('restricciones_alimentarias'):
                lines.append(f"Restricciones: {patient['restricciones_alimentarias']}")

            if patient.get('alergias'):
                lines.append(f"Alergias: {patient['alergias']}")

            lines.append("")

        return "\n".join(lines)
