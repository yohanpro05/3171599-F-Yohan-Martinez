"""
Schemas Pydantic
================
Define los modelos de datos para validación en e-commerce de libros usados.
# QUE: Actualizada descripción.
# PARA: Contextualizar.
# IMPACTO: Docs.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
# ============================================
# ENUMS
# ============================================
class SortOrder(str, Enum):
    """Orden de clasificación"""
    asc = "asc"
    desc = "desc"

class BookSortField(str, Enum):  # QUE: Cambiado ProductSortField a BookSortField; agregados author, publication_year.
    # PARA: Ordenamiento relevante a libros.
    # IMPACTO: Usado en dependencies y routers; expande opciones.
    name = "name"
    price = "price"
    created_at = "created_at"
    stock = "stock"
    author = "author"
    publication_year = "publication_year"

# ============================================
# GENRE SCHEMAS (antes Category)
# ============================================
class GenreBase(BaseModel):  # QUE: Cambiado CategoryBase a GenreBase.
    # PARA: Adaptar.
    # IMPACTO: Afecta todos los schemas relacionados.
    """Schema base para géneros"""
    name: str = Field(..., min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=200)

class GenreCreate(GenreBase):
    """Schema para crear género"""
    pass

class GenreUpdate(BaseModel):
    """Schema para actualizar género"""
    name: str | None = Field(None, min_length=2, max_length=50)
    description: str | None = Field(None, max_length=200)

class GenreResponse(GenreBase):
    """Schema de respuesta para género"""
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}

# ============================================
# BOOK SCHEMAS (antes Product)
# ============================================
class BookBase(BaseModel):  # QUE: Cambiado ProductBase a BookBase; agregados author, publication_year, isbn, condition; removido tags.
    # PARA: Campos específicos de libros usados.
    # IMPACTO: Validación ahora incluye estos; afecta DB y routers.
    """Schema base para libros"""
    name: str = Field(..., min_length=2, max_length=100, description="Title of the book")
    description: str | None = Field(default=None, max_length=500)
    price: float = Field(..., gt=0)
    author: str = Field(..., min_length=2, max_length=100)
    publication_year: int = Field(..., ge=1000, le=datetime.now().year)
    isbn: str | None = Field(default=None, pattern=r"^\d{10,13}$", description="ISBN 10 or 13 digits")
    condition: str = Field(..., examples=["nuevo", "bueno", "regular"])
    stock: int = Field(default=0, ge=0)

class BookCreate(BookBase):
    """Schema para crear libro"""
    genre_id: int = Field(..., gt=0)  # QUE: Cambiado category_id a genre_id.
    # PARA: Consistencia.
    # IMPACTO: Validación en creación.

class BookUpdate(BaseModel):
    """Schema para actualización parcial"""
    name: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = Field(None, max_length=500)
    price: float | None = Field(None, gt=0)
    author: str | None = Field(None, min_length=2, max_length=100)
    publication_year: int | None = Field(None, ge=1000, le=datetime.now().year)
    isbn: str | None = Field(None, pattern=r"^\d{10,13}$")
    condition: str | None = None
    stock: int | None = Field(None, ge=0)
    genre_id: int | None = Field(None, gt=0)

class BookResponse(BookBase):
    """Schema de respuesta para libro"""
    id: int
    genre_id: int
    created_at: datetime
    genre: GenreResponse | None = None  # QUE: Cambiado category a genre.
    # PARA: Incluir datos de género.
    # IMPACTO: Respuestas más ricas.

# ============================================
# PAGINATION SCHEMAS
# ============================================
class PaginatedResponse(BaseModel):
    """Schema para respuestas paginadas"""
    items: list[BookResponse]  # QUE: Cambiado a BookResponse.
    # PARA: Adaptar a libros.
    # IMPACTO: Tipado en respuestas paginadas.
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool