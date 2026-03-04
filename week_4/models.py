"""
QUE:    Define todos los esquemas Pydantic para validación de entrada, serialización de salida y documentación automática en OpenAPI.
PARA:   Servir como contrato claro entre la API y los clientes: validar datos entrantes (create/update), estructurar respuestas seguras y consistentes, y generar schemas detallados en /docs para que el evaluador y otros desarrolladores entiendan exactamente qué datos se esperan y devuelven.
IMPACTO: Si están bien diseñados → validación automática fuerte, documentación profesional en Swagger (con ejemplos útiles), respuestas predecibles y seguras / Si están incompletos o mal tipados → errores 422 frecuentes, documentación confusa, riesgo de exponer datos sensibles y baja puntuación en "Response models bien diseñados" (10 puntos clave).
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List

from pydantic import BaseModel, Field, ConfigDict


# ============================================
# ENUMS - Estados y Condiciones del negocio
# ============================================

class ListingStatus(str, Enum):
    """Estados posibles de un anuncio de libro usado"""
    AVAILABLE = "available"
    RESERVED  = "reserved"
    SOLD      = "sold"
    CANCELLED = "cancelled"


class BookCondition(str, Enum):
    """Condición física del libro (importante para compradores de usados)"""
    EXCELLENT   = "excellent"
    VERY_GOOD   = "very_good"
    GOOD        = "good"
    FAIR        = "fair"
    ACCEPTABLE  = "acceptable"


# ============================================
# ERROR SCHEMAS
# ============================================

class ErrorDetail(BaseModel):
    """Detalle de error interno"""
    code: str = Field(..., description="Código único del error")
    message: str = Field(..., description="Mensaje descriptivo")
    details: dict | None = Field(None, description="Detalles adicionales")


class ErrorResponse(BaseModel):
    """Respuesta de error estándar"""
    error: ErrorDetail
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": {
                    "code": "LISTING_NOT_FOUND",
                    "message": "Anuncio con id 99 no encontrado",
                    "details": None
                }
            }
        }
    )


# ============================================
# SCHEMAS DE ANUNCIO
# ============================================

class ListingCreate(BaseModel):
    """
    Schema para crear un nuevo anuncio de libro usado.
    """
    title: str = Field(..., min_length=3, max_length=200, description="Título del libro")
    author: str = Field(..., min_length=2, max_length=100, description="Nombre del autor")
    isbn: Optional[str] = Field(None, pattern=r"^\d{10}(\d{3})?$", description="ISBN-10 o ISBN-13 (opcional)")
    publication_year: Optional[int] = Field(None, ge=1800, le=2026, description="Año de publicación")
    price: float = Field(..., gt=1000, description="Precio en COP")
    condition: BookCondition = Field(default=BookCondition.GOOD, description="Estado físico del libro")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción adicional")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Cien años de soledad",
                "author": "Gabriel García Márquez",
                "isbn": "9788437604947",
                "publication_year": 1967,
                "price": 45000.0,
                "condition": "very_good",
                "description": "Edición de bolsillo, páginas amarillentas pero sin marcas."
            }
        }
    )


class ListingUpdate(BaseModel):
    """
    Schema para actualización completa (PUT) de un anuncio. Todos los campos opcionales.
    """
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    author: Optional[str] = Field(None, min_length=2, max_length=100)
    isbn: Optional[str] = Field(None, pattern=r"^\d{10}(\d{3})?$")
    publication_year: Optional[int] = Field(None, ge=1800, le=2026)
    price: Optional[float] = Field(None, gt=1000)
    condition: Optional[BookCondition] = None
    description: Optional[str] = Field(None, max_length=1000)


class StatusUpdate(BaseModel):
    """
    Schema para cambiar solo el estado del anuncio (PATCH /listings/{id}/status)
    """
    status: ListingStatus = Field(..., description="Nuevo estado del anuncio")


class ListingResponse(BaseModel):
    """
    Schema de respuesta básica (público) para un anuncio.
    """
    id: int
    title: str
    author: str
    price: float
    condition: BookCondition
    status: ListingStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Cien años de soledad",
                "author": "Gabriel García Márquez",
                "price": 45000.0,
                "condition": "very_good",
                "status": "available",
                "created_at": "2026-03-03T23:00:00"
            }
        }
    )


class ListingDetailResponse(ListingResponse):
    """
    Schema de respuesta detallada (para GET /listings/{id}).
    Incluye campos adicionales que no se muestran en la lista.
    """
    isbn: Optional[str]
    publication_year: Optional[int]
    description: Optional[str]
    updated_at: Optional[datetime]
    reserved_at: Optional[datetime]
    sold_at: Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Cien años de soledad",
                "author": "Gabriel García Márquez",
                "isbn": "9788437604947",
                "publication_year": 1967,
                "price": 45000.0,
                "condition": "very_good",
                "description": "Edición de bolsillo, páginas amarillentas pero sin marcas.",
                "status": "available",
                "created_at": "2026-03-03T23:00:00",
                "updated_at": None,
                "reserved_at": None,
                "sold_at": None
            }
        }
    )


class ListingListResponse(BaseModel):
    """
    Schema para listado paginado de anuncios.
    """
    items: List[ListingResponse]
    total: int
    skip: int
    limit: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [
                    {
                        "id": 1,
                        "title": "Cien años de soledad",
                        "author": "Gabriel García Márquez",
                        "price": 45000.0,
                        "condition": "very_good",
                        "status": "available",
                        "created_at": "2026-03-03T23:00:00"
                    }
                ],
                "total": 1,
                "skip": 0,
                "limit": 20
            }
        }
    )


class ListingStats(BaseModel):
    """
    Schema para estadísticas generales del catálogo.
    """
    total_listings: int
    by_status: Dict[str, int]          # ej: {"available": 15, "sold": 3}
    average_price: float
    max_price: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_listings": 25,
                "by_status": {
                    "available": 18,
                    "reserved": 4,
                    "sold": 3,
                    "cancelled": 0
                },
                "average_price": 38500.75,
                "max_price": 120000.0
            }
        }
    )