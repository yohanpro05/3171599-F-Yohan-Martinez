"""
Schemas Pydantic para la API de Libros
=========================================

TODO: Implementar los schemas según las especificaciones del proyecto.

Schemas requeridos:
- BookBase: Campos comunes
- BookCreate: Para POST (con validadores)
- BookUpdate: Para PATCH (todos opcionales)
- BookResponse: Para respuestas
- BookList: Lista paginada
"""


from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
import re


# ============================================
# TODO 1: BookBase
# Campos comunes para todos los schemas de libro
# ============================================

class BookBase(BaseModel):
    """
    Campos comunes para libros usados.
    
    Campos:
    - title: str (3-200 caracteres)
    - author: str (2-100 caracteres)
    - isbn: str | None (ISBN-10 o ISBN-13 válido)
    - publisher: str | None
    - publication_year: int | None (1500-actual)
    - condition: str (enum: new, like_new, good, fair, poor)
    - price: float (> 0)
    - currency: str (COP por defecto)
    - stock: int (>= 0, default 1)
    - description: str | None (máx 2000 caracteres)
    - genres: list[str] (máximo 8, default [])
    - is_featured: bool = False
    """
    title: str = Field(..., min_length=3, max_length=200)
    author: str = Field(..., min_length=2, max_length=100)
    isbn: Optional[str] = Field(
        None,
        pattern=r"^(97[89])?\d{9}(\d|X)$",
        description="ISBN-10 o ISBN-13 (sin guiones)"
    )
    publisher: Optional[str] = Field(None, max_length=100)
    publication_year: Optional[int] = Field(None, ge=1500, le=datetime.now().year + 1)
    condition: Literal["new", "like_new", "good", "fair", "poor"] = "good"
    price: float = Field(..., gt=0, description="Precio en la moneda indicada")
    currency: Literal["COP", "USD", "EUR"] = "COP"
    stock: int = Field(default=1, ge=0)
    description: Optional[str] = Field(None, max_length=2000)
    genres: List[str] = Field(default_factory=list, max_items=8)
    is_featured: bool = Field(default=False)


# ============================================
# TODO 2: BookCreate
# Schema para crear libros (POST)
# Incluye validadores para normalizar datos
# ============================================

class BookCreate(BookBase):
    """
    Schema para crear un libro usado.
    
    Validadores requeridos:
    1. normalize_names: Capitalizar title y author
    2. normalize_genres: Minúsculas, sin duplicados, máximo 8
    """

    @field_validator('title', 'author')
    @classmethod
    def normalize_text(cls, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned) < 2:
            raise ValueError("debe tener al menos 2 caracteres después de quitar espacios")
        return cleaned.title()

    @field_validator('genres')
    @classmethod
    def normalize_genres(cls, value: list) -> list:
        if not value:
            return []
        lowered = [genre.lower().strip() for genre in value]
        unique = list(dict.fromkeys(lowered))
        return unique[:8]


# ============================================
# TODO 3: BookUpdate
# Schema para actualizar libros parcialmente (PATCH)
# Todos los campos son opcionales
# ============================================

class BookUpdate(BaseModel):
    """
    Schema para actualizar libro parcialmente.
    
    Todos los campos son opcionales (None por defecto).
    Incluir los mismos validadores que BookCreate (adaptados).
    """
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    publication_year: Optional[int] = None
    condition: Optional[Literal["new", "like_new", "good", "fair", "poor"]] = None
    price: Optional[float] = Field(None, gt=0)
    currency: Optional[Literal["COP", "USD", "EUR"]] = None
    stock: Optional[int] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=2000)
    genres: Optional[List[str]] = None
    is_featured: Optional[bool] = None

    @field_validator('title', 'author')
    @classmethod
    def normalize_text(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        cleaned = value.strip()
        if len(cleaned) < 2:
            raise ValueError("debe tener al menos 2 caracteres")
        return cleaned.title()

    @field_validator('genres')
    @classmethod
    def normalize_genres(cls, value: Optional[list]) -> Optional[list]:
        if value is None:
            return None
        if not value:
            return []
        lowered = [genre.lower().strip() for genre in value]
        unique = list(dict.fromkeys(lowered))
        return unique[:8]


# ============================================
# TODO 4: BookResponse
# Schema para respuestas (incluye id y timestamps)
# ============================================

class BookResponse(BookBase):
    """
    Schema para respuestas de libro.
    
    Campos adicionales:
    - id: int
    - created_at: datetime
    - updated_at: datetime | None
    
    Configuración:
    - from_attributes=True (para compatibilidad con ORM futuro)
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


# ============================================
# Lista paginada (para GET /books)
# ============================================

class BookList(BaseModel):
    """
    Respuesta paginada de libros
    """
    items: List[BookResponse]
    total: int
    page: int
    per_page: int
