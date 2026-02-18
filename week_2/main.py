"""
Proyecto Semana 02: API de Gestión de Libros Usados
===================================================

Aplicación FastAPI principal.
Los endpoints ya están definidos, debes completar schemas.py

Ejecutar:
    docker compose up --build
    
Documentación: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, status, Query
from datetime import datetime

# TODO: Importar los schemas que crearás
from schemas import (
    BookCreate,
    BookUpdate,
    BookResponse,
    BookList,
)
from database import books_db, get_next_id, find_by_isbn

app = FastAPI(
    title="API de Gestión de Libros Usados",
    description="Proyecto Semana 02 - Pydantic v2",
    version="1.0.0",
)


# ============================================
# ENDPOINTS
# ============================================

@app.post(
    "/books",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Books"],
)
async def create_book(book: BookCreate) -> BookResponse:
    """
    Crear un nuevo libro usado.
    
    - Valida que el ISBN no exista (si se proporciona)
    - Normaliza título, autor y géneros
    """
    # Verificar ISBN único
    if book.isbn and find_by_isbn(book.isbn):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un libro con el ISBN {book.isbn}"
        )
    
    # Crear libro
    book_id = get_next_id()
    new_book = {
        "id": book_id,
        **book.model_dump(),
        "created_at": datetime.now(),
        "updated_at": None,
    }
    books_db[book_id] = new_book
    
    return BookResponse(**new_book)


@app.get(
    "/books",
    response_model=BookList,
    tags=["Books"],
)
async def list_books(
    page: int = Query(ge=1, default=1),
    per_page: int = Query(ge=1, le=100, default=10),
    featured_only: bool = False,
) -> BookList:
    """
    Listar libros con paginación.
    
    - Soporta filtro por libros destacados
    """
    # Filtrar
    books = list(books_db.values())
    if featured_only:
        books = [b for b in books if b["is_featured"]]
    
    # Paginar
    total = len(books)
    start = (page - 1) * per_page
    end = start + per_page
    items = books[start:end]
    
    return BookList(
        items=[BookResponse(**b) for b in items],
        total=total,
        page=page,
        per_page=per_page,
    )


@app.get(
    "/books/{book_id}",
    response_model=BookResponse,
    tags=["Books"],
)
async def get_book(book_id: int) -> BookResponse:
    """Obtener libro por ID."""
    if book_id not in books_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return BookResponse(**books_db[book_id])


@app.patch(
    "/books/{book_id}",
    response_model=BookResponse,
    tags=["Books"],
)
async def update_book(
    book_id: int,
    book: BookUpdate,
) -> BookResponse:
    """
    Actualizar libro parcialmente.
    
    - Solo actualiza campos enviados
    - Valida ISBN único si se cambia
    """
    if book_id not in books_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Obtener solo campos enviados
    update_data = book.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    # Si se actualiza ISBN, verificar que no exista
    if "isbn" in update_data:
        existing = find_by_isbn(update_data["isbn"])
        if existing and existing["id"] != book_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"ISBN {update_data['isbn']} already in use"
            )
    
    # Actualizar
    stored = books_db[book_id]
    for key, value in update_data.items():
        stored[key] = value
    stored["updated_at"] = datetime.now()
    
    return BookResponse(**stored)


@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Books"],
)
async def delete_book(book_id: int) -> None:
    """Eliminar libro."""
    if book_id not in books_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    del books_db[book_id]


@app.post(
    "/books/{book_id}/featured",
    response_model=BookResponse,
    tags=["Books"],
)
async def toggle_featured(book_id: int) -> BookResponse:
    """Toggle featured status."""
    if book_id not in books_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    stored = books_db[book_id]
    stored["is_featured"] = not stored["is_featured"]
    stored["updated_at"] = datetime.now()
    
    return BookResponse(**stored)


# ============================================
# HEALTH CHECK
# ============================================

@app.get("/", tags=["Health"])
async def root():
    """Health check."""
    return {
        "status": "ok",
        "message": "Books API running",
        "total_books": len(books_db),
    }
