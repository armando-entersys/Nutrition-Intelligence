"""
RAG Search Service
==================

Servicio de búsqueda para el sistema RAG.
Proporciona búsqueda de productos, alimentos e historial.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy import select, func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.foods.nom051_models import ProductoNOM051, FoodSMAE
from domain.auth.models import AuthUser


class RAGSearchService:
    """
    Servicio de búsqueda para RAG

    Proporciona funcionalidades de búsqueda en:
    - Productos NOM-051
    - Alimentos SMAE
    - Historial de usuario
    - Datos de pacientes (para nutriólogos)
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def search_products(
        self,
        query: str,
        user_id: Optional[int] = None,
        limit: int = 10,
        verified_only: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Buscar productos NOM-051

        Args:
            query: Texto de búsqueda
            user_id: ID del usuario (opcional, para filtrar productos privados)
            limit: Número máximo de resultados
            verified_only: Solo productos verificados

        Returns:
            Lista de productos encontrados
        """
        # Construir query base
        stmt = select(ProductoNOM051)

        # Filtros de búsqueda por texto usando pg_trgm
        # Buscar en nombre, marca, ingredientes
        search_filter = or_(
            func.similarity(ProductoNOM051.nombre, query) > 0.3,
            func.similarity(ProductoNOM051.marca, query) > 0.3,
            ProductoNOM051.nombre.ilike(f"%{query}%"),
            ProductoNOM051.marca.ilike(f"%{query}%"),
        )

        stmt = stmt.where(search_filter)

        # Filtro de productos verificados
        if verified_only:
            stmt = stmt.where(ProductoNOM051.verified == True)

        # Solo productos globales o del usuario actual
        if user_id:
            stmt = stmt.where(
                or_(
                    ProductoNOM051.is_global == True,
                    ProductoNOM051.created_by_user_id == user_id,
                )
            )
        else:
            stmt = stmt.where(ProductoNOM051.is_global == True)

        # Ordenar por relevancia (similarity + scan_count)
        stmt = stmt.order_by(
            (func.similarity(ProductoNOM051.nombre, query) * 0.7 +
             (ProductoNOM051.scan_count / 100.0) * 0.3).desc()
        )

        stmt = stmt.limit(limit)

        result = await self.session.execute(stmt)
        products = result.scalars().all()

        return [self._product_to_dict(p) for p in products]

    async def search_foods(
        self,
        query: str,
        limit: int = 10,
        category: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Buscar alimentos en base SMAE

        Args:
            query: Texto de búsqueda
            limit: Número máximo de resultados
            category: Categoría de alimento (opcional)

        Returns:
            Lista de alimentos encontrados
        """
        stmt = select(FoodSMAE)

        # Búsqueda por similitud de texto
        search_filter = or_(
            func.similarity(FoodSMAE.nombre_alimento, query) > 0.3,
            FoodSMAE.nombre_alimento.ilike(f"%{query}%"),
        )

        stmt = stmt.where(search_filter)

        # Filtro por categoría
        if category:
            stmt = stmt.where(FoodSMAE.grupo_alimento == category)

        # Ordenar por relevancia
        stmt = stmt.order_by(
            func.similarity(FoodSMAE.nombre_alimento, query).desc()
        )

        stmt = stmt.limit(limit)

        result = await self.session.execute(stmt)
        foods = result.scalars().all()

        return [self._food_to_dict(f) for f in foods]

    async def get_user_scan_history(
        self,
        user_id: int,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Obtener historial de escaneos del usuario

        Args:
            user_id: ID del usuario
            limit: Número máximo de resultados

        Returns:
            Lista de escaneos con productos
        """
        # Query al historial de escaneos
        query = """
        SELECT
            sh.id,
            sh.user_id,
            sh.scanned_at,
            sh.source,
            p.codigo_barras,
            p.nombre,
            p.marca,
            p.health_score,
            p.health_level,
            p.calorias,
            p.azucares,
            p.grasas_saturadas,
            p.sodio,
            p.exceso_calorias,
            p.exceso_azucares,
            p.exceso_grasas_saturadas,
            p.exceso_sodio
        FROM user_scan_history sh
        JOIN productos_nom051 p ON sh.product_id = p.id
        WHERE sh.user_id = :user_id
        ORDER BY sh.scanned_at DESC
        LIMIT :limit
        """

        result = await self.session.execute(
            query,
            {"user_id": user_id, "limit": limit}
        )

        return [dict(row) for row in result.mappings()]

    async def get_user_favorite_foods(
        self,
        user_id: int,
    ) -> List[Dict[str, Any]]:
        """
        Obtener alimentos favoritos del usuario

        Args:
            user_id: ID del usuario

        Returns:
            Lista de alimentos favoritos
        """
        query = """
        SELECT
            ff.id,
            ff.user_id,
            ff.created_at,
            f.id as food_id,
            f.nombre_alimento,
            f.grupo_alimento,
            f.energia_kcal,
            f.proteinas_g,
            f.carbohidratos_g,
            f.fibra_g,
            f.grasas_totales_g
        FROM favorite_foods ff
        JOIN foods_smae f ON ff.food_id = f.id
        WHERE ff.user_id = :user_id
        ORDER BY ff.created_at DESC
        """

        result = await self.session.execute(
            query,
            {"user_id": user_id}
        )

        return [dict(row) for row in result.mappings()]

    async def search_combined(
        self,
        query: str,
        user_id: Optional[int] = None,
        search_products: bool = True,
        search_foods: bool = True,
        limit_per_source: int = 5,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Búsqueda combinada en productos y alimentos

        Args:
            query: Texto de búsqueda
            user_id: ID del usuario
            search_products: Buscar en productos
            search_foods: Buscar en alimentos
            limit_per_source: Límite por fuente de datos

        Returns:
            Diccionario con resultados de ambas fuentes
        """
        results = {
            "products": [],
            "foods": [],
        }

        if search_products:
            results["products"] = await self.search_products(
                query=query,
                user_id=user_id,
                limit=limit_per_source,
            )

        if search_foods:
            results["foods"] = await self.search_foods(
                query=query,
                limit=limit_per_source,
            )

        return results

    def _product_to_dict(self, product: ProductoNOM051) -> Dict[str, Any]:
        """Convertir producto a diccionario"""
        return {
            "id": product.id,
            "codigo_barras": product.codigo_barras,
            "nombre": product.nombre,
            "marca": product.marca,
            "calorias": product.calorias,
            "azucares": product.azucares,
            "grasas_saturadas": product.grasas_saturadas,
            "grasas_trans": product.grasas_trans,
            "sodio": product.sodio,
            "proteinas": product.proteinas,
            "carbohidratos": product.carbohidratos,
            "fibra": product.fibra,
            "exceso_calorias": product.exceso_calorias,
            "exceso_azucares": product.exceso_azucares,
            "exceso_grasas_saturadas": product.exceso_grasas_saturadas,
            "exceso_grasas_trans": product.exceso_grasas_trans,
            "exceso_sodio": product.exceso_sodio,
            "health_score": product.health_score,
            "health_level": product.health_level,
            "scan_count": product.scan_count,
            "verified": product.verified,
            "is_global": product.is_global,
        }

    def _food_to_dict(self, food: FoodSMAE) -> Dict[str, Any]:
        """Convertir alimento a diccionario"""
        return {
            "id": food.id,
            "cve_alimento": food.cve_alimento,
            "nombre_alimento": food.nombre_alimento,
            "grupo_alimento": food.grupo_alimento,
            "energia_kcal": food.energia_kcal,
            "proteinas_g": food.proteinas_g,
            "carbohidratos_g": food.carbohidratos_g,
            "fibra_g": food.fibra_g,
            "grasas_totales_g": food.grasas_totales_g,
            "acidos_grasos_saturados_g": food.acidos_grasos_saturados_g,
            "colesterol_mg": food.colesterol_mg,
            "sodio_mg": food.sodio_mg,
        }
