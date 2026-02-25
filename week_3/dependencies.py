"""
Dependencias Reutilizables
==========================
Define dependencias para paginación, filtros y ordenamiento de libros usados.
# QUE: Actualizada descripción.
# PARA: Contextualizar.
# IMPACTO: Docs.
"""
from fastapi import Query, Depends
from typing import Annotated
from schemas import SortOrder, BookSortField  # QUE: Cambiado ProductSortField a BookSortField.
# PARA: Campos de orden ahora incluyen author, publication_year.
# IMPACTO: Enums deben actualizarse en schemas.
# ============================================
# PAGINACIÓN
# ============================================
class PaginationParams:
    """
    Dependencia para parámetros de paginación.
    """
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Page number"),
        per_page: int = Query(default=10, ge=1, le=50, description="Items per page")
    ):
        self.page = page
        self.per_page = per_page
        self.offset = (page - 1) * per_page

PaginationDep = Annotated[PaginationParams, Depends()]

# ============================================
# FILTROS DE LIBROS
# ============================================
class BookFilters:  # QUE: Cambiado ProductFilters a BookFilters.
    # PARA: Adaptar.
    # IMPACTO: Usado en routers.
    """
    Dependencia para filtros de libros.
    """
    def __init__(
        self,
        search: str | None = Query(default=None, min_length=2, description="Search in name, description, author"),
        genre_id: int | None = Query(default=None, gt=0, description="Filter by genre ID"),  # QUE: Cambiado category_id a genre_id.
        # PARA: Consistencia.
        # IMPACTO: Cambia params de query.
        min_price: float | None = Query(default=None, ge=0, description="Minimum price"),
        max_price: float | None = Query(default=None, ge=0, description="Maximum price"),
        in_stock: bool | None = Query(default=None, description="Filter in stock books"),
        min_year: int | None = Query(default=None, ge=0, description="Minimum publication year"),  # QUE: Agregados min_year y condition.
        # PARA: Filtros específicos de libros.
        # IMPACTO: Mejora búsqueda; implementado en products.py.
        condition: str | None = Query(default=None, description="Book condition (e.g., bueno, regular)")
    ):
        self.search = search
        self.genre_id = genre_id
        self.min_price = min_price
        self.max_price = max_price
        self.in_stock = in_stock
        self.min_year = min_year
        self.condition = condition

BookFiltersDep = Annotated[BookFilters, Depends()]

# ============================================
# ORDENAMIENTO
# ============================================
class SortingParams:
    """
    Dependencia para ordenamiento.
    """
    def __init__(
        self,
        sort_by: BookSortField = Query(default=BookSortField.name, description="Field to sort by"),
        order: SortOrder = Query(default=SortOrder.asc, description="Sort order")
    ):
        self.sort_by = sort_by
        self.order = order

SortingDep = Annotated[SortingParams, Depends()]