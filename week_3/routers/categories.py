"""
Router de Géneros de Libros
===========================
CRUD completo para géneros de libros usados.
# QUE: Cambiado título de "Categorías" a "Géneros de Libros".
# PARA: Adaptar al dominio de libros usados, donde categorías son géneros.
# IMPACTO: Mejora la semántica; no afecta funcionalidad, solo documentación.
"""
from fastapi import APIRouter, Path, HTTPException, status
from datetime import datetime
from database import genres_db, get_next_genre_id  # QUE: Cambiado categories_db a genres_db y get_next_category_id a get_next_genre_id.
# PARA: Consistencia con nuevo dominio (géneros en lugar de categorías).
# IMPACTO: Evita confusiones; requiere cambios en database.py para coincidir.
from schemas import GenreCreate, GenreUpdate, GenreResponse  # QUE: Cambiados nombres de schemas de Category* a Genre*.
# PARA: Reflejar que ahora son géneros de libros.
# IMPACTO: Schemas deben actualizarse; rompe compatibilidad con original si no se adapta todo.
router = APIRouter(
    prefix="/genres",
    tags=["Genres"],
    responses={404: {"description": "Genre not found"}}  # QUE: Cambiado "Category" a "Genre" en tags y responses.
    # PARA: Adaptar terminología.
    # IMPACTO: Mejora UX en docs de Swagger.
)
# ============================================
# GET /genres - Listar todas
# ============================================
@router.get("/", response_model=list[GenreResponse])
async def list_genres():
    """
    Listar todos los géneros de libros.
   
    # QUE: Implementado retorno de todas las entradas en genres_db.
    # PARA: Completar el TODO original.
    # IMPACTO: Permite listar géneros; expone toda la DB.
    """
    return list(genres_db.values())

# ============================================
# GET /genres/{id} - Obtener una
# ============================================
@router.get("/{genre_id}", response_model=GenreResponse)
async def get_genre(
    genre_id: int = Path(..., gt=0, description="Genre ID")  # QUE: Cambiado category_id a genre_id.
    # PARA: Consistencia con dominio.
    # IMPACTO: Cambia la ruta y params; clientes deben actualizar llamadas.
):
    """
    Obtener un género por ID.
    """
    if genre_id not in genres_db:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genres_db[genre_id]

# ============================================
# POST /genres - Crear
# ============================================
@router.post("/", response_model=GenreResponse, status_code=status.HTTP_201_CREATED)
async def create_genre(genre: GenreCreate):
    """
    Crear un nuevo género.
    """
    new_id = get_next_genre_id()
    new_genre = {
        "id": new_id,
        **genre.model_dump(),
        "created_at": datetime.now()
    }
    genres_db[new_id] = new_genre
    return new_genre

# ============================================
# PUT /genres/{id} - Actualizar completo
# ============================================
@router.put("/{genre_id}", response_model=GenreResponse)
async def update_genre(
    genre_id: int = Path(..., gt=0),
    genre: GenreCreate = ...
):
    """
    Actualizar un género completamente.
    """
    if genre_id not in genres_db:
        raise HTTPException(status_code=404, detail="Genre not found")
    updated_genre = {
        "id": genre_id,
        **genre.model_dump(),
        "created_at": genres_db[genre_id]["created_at"]
    }
    genres_db[genre_id] = updated_genre
    return updated_genre

# ============================================
# DELETE /genres/{id} - Eliminar
# ============================================
@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre(
    genre_id: int = Path(..., gt=0)
):
    """
    Eliminar un género.
    """
    if genre_id not in genres_db:
        raise HTTPException(status_code=404, detail="Genre not found")
    del genres_db[genre_id]
    return None