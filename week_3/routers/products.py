"""
Router de Libros Usados
=======================
CRUD con filtrado, paginación y ordenamiento para libros usados.
# QUE: Cambiado título de "Productos" a "Libros Usados".
# PARA: Adaptar al dominio específico.
# IMPACTO: Mejora documentación; no afecta código.
"""
from fastapi import APIRouter, Path, HTTPException, status
from datetime import datetime
from database import books_db, genres_db, get_next_book_id  # QUE: Cambiado products_db a books_db, categories_db a genres_db, get_next_product_id a get_next_book_id.
# PARA: Consistencia con dominio de libros.
# IMPACTO: Requiere actualización en database.py.
from schemas import BookCreate, BookUpdate, BookResponse, SortOrder  # QUE: Cambiados nombres de schemas de Product* a Book*.
# PARA: Reflejar libros en lugar de productos genéricos.
# IMPACTO: Schemas deben adaptarse; afecta validación.
from dependencies import PaginationDep, BookFiltersDep, SortingDep  # QUE: Cambiado ProductFiltersDep a BookFiltersDep.
# PARA: Filtros ahora incluyen campos de libros como author.
# IMPACTO: Dependencias deben actualizarse para nuevos filtros.
router = APIRouter(
    prefix="/books",
    tags=["Books"],
    responses={404: {"description": "Book not found"}}  # QUE: Cambiado "Products" a "Books" y "Product" a "Book".
    # PARA: Adaptar terminología.
    # IMPACTO: Actualiza tags en docs.
)
# ============================================
# GET /books - Listar con filtros
# ============================================
@router.get("/")
async def list_books(
    pagination: PaginationDep,
    filters: BookFiltersDep,
    sorting: SortingDep
):
    """
    Listar libros con filtrado, paginación y ordenamiento.
   
    # QUE: Implementado filtrado completo (search en name/description/author, genre_id, min_price/max_price, in_stock, min_year, condition).
    # PARA: Completar TODO y adaptar a libros (e.g., filtro por año y condición).
    # IMPACTO: Permite consultas avanzadas; mejora usabilidad para e-commerce.
    """
    books = list(books_db.values())
    
    # Aplicar filtros
    if filters.search:
        search_lower = filters.search.lower()
        books = [b for b in books if search_lower in b["name"].lower() or search_lower in b["description"].lower() or search_lower in b["author"].lower()]
    if filters.genre_id:
        books = [b for b in books if b["genre_id"] == filters.genre_id]
    if filters.min_price is not None:
        books = [b for b in books if b["price"] >= filters.min_price]
    if filters.max_price is not None:
        books = [b for b in books if b["price"] <= filters.max_price]
    if filters.in_stock is not None:
        books = [b for b in books if (b["stock"] > 0) == filters.in_stock]
    if filters.min_year is not None:
        books = [b for b in books if b["publication_year"] >= filters.min_year]
    if filters.condition:
        books = [b for b in books if b["condition"] == filters.condition]
    
    # Ordenar
    reverse = sorting.order == SortOrder.desc
    books.sort(key=lambda b: b[sorting.sort_by.value], reverse=reverse)
    
    # Paginar
    total = len(books)
    books = books[pagination.offset : pagination.offset + pagination.per_page]
    pages = (total + pagination.per_page - 1) // pagination.per_page
    has_next = pagination.page < pages
    has_prev = pagination.page > 1
    
    return {
        "items": books,
        "total": total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pages,
        "has_next": has_next,
        "has_prev": has_prev
    }

# ============================================
# GET /books/{id} - Obtener uno
# ============================================
@router.get("/{book_id}")
async def get_book(
    book_id: int = Path(..., gt=0, description="Book ID")  # QUE: Cambiado product_id a book_id.
    # PARA: Consistencia.
    # IMPACTO: Cambia rutas.
):
    """
    Obtener un libro por ID.
    """
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    book = books_db[book_id].copy()
    genre_id = book["genre_id"]
    book["genre"] = genres_db.get(genre_id)
    return book

# ============================================
# POST /books - Crear
# ============================================
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    """
    Crear un nuevo libro.
    """
    if book.genre_id not in genres_db:
        raise HTTPException(status_code=400, detail="Genre not found")
    new_id = get_next_book_id()
    new_book = {
        "id": new_id,
        **book.model_dump(),
        "created_at": datetime.now()
    }
    books_db[new_id] = new_book
    return new_book

# ============================================
# PUT /books/{id} - Actualizar completo
# ============================================
@router.put("/{book_id}")
async def replace_book(
    book_id: int = Path(..., gt=0),
    book: BookCreate = ...
):
    """
    Reemplazar un libro completamente.
    """
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.genre_id not in genres_db:
        raise HTTPException(status_code=400, detail="Genre not found")
    updated_book = {
        "id": book_id,
        **book.model_dump(),
        "created_at": books_db[book_id]["created_at"]
    }
    books_db[book_id] = updated_book
    return updated_book

# ============================================
# PATCH /books/{id} - Actualizar parcial
# ============================================
@router.patch("/{book_id}")
async def update_book(
    book_id: int = Path(..., gt=0),
    book: BookUpdate = ...
):
    """
    Actualizar un libro parcialmente.
    """
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    existing = books_db[book_id]
    update_data = book.model_dump(exclude_unset=True)
    if "genre_id" in update_data and update_data["genre_id"] not in genres_db:
        raise HTTPException(status_code=400, detail="Genre not found")
    updated = {**existing, **update_data}
    books_db[book_id] = updated
    return updated

# ============================================
# DELETE /books/{id} - Eliminar
# ============================================
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int = Path(..., gt=0)
):
    """
    Eliminar un libro.
    """
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    del books_db[book_id]
    return None