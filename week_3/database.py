"""
Base de Datos Simulada
======================
Datos en memoria para el e-commerce de libros usados.
# QUE: Cambiado descripción para reflejar dominio.
# PARA: Contextualizar.
# IMPACTO: Solo docs.
"""
from datetime import datetime
# ============================================
# GÉNEROS DE LIBROS
# ============================================
genres_db: dict[int, dict] = {  # QUE: Cambiado categories_db a genres_db.
    # PARA: Adaptar a géneros de libros.
    # IMPACTO: Cambia clave de acceso en routers.
    1: {
        "id": 1,
        "name": "Ficción",
        "description": "Novelas y cuentos ficticios",
        "created_at": datetime(2024, 1, 1, 10, 0, 0)
    },
    2: {
        "id": 2,
        "name": "No Ficción",
        "description": "Biografías, ensayos y libros informativos",
        "created_at": datetime(2024, 1, 1, 10, 0, 0)
    },
    3: {
        "id": 3,
        "name": "Misterio",
        "description": "Libros de suspense y detectives",
        "created_at": datetime(2024, 1, 1, 10, 0, 0)
    },
    4: {
        "id": 4,
        "name": "Ciencia Ficción",
        "description": "Historias futuristas y especulativas",
        "created_at": datetime(2024, 1, 1, 10, 0, 0)
    },
}  # QUE: Cambiados ejemplos de categorías a géneros de libros.
# PARA: Relevancia al dominio.
# IMPACTO: Datos iniciales ahora son temáticos; afecta pruebas.
next_genre_id = 5  # QUE: Cambiado next_category_id a next_genre_id.
# PARA: Consistencia.
# IMPACTO: Afecta generación de IDs.

# ============================================
# LIBROS USADOS
# ============================================
books_db: dict[int, dict] = {  # QUE: Cambiado products_db a books_db.
    # PARA: Adaptar a libros.
    # IMPACTO: Cambia acceso en código.
    1: {
        "id": 1,
        "name": "1984",
        "description": "Clásico distópico de George Orwell",
        "price": 12.99,
        "genre_id": 4,  # QUE: Cambiado category_id a genre_id.
        # PARA: Consistencia.
        # IMPACTO: Requiere actualización en schemas y routers.
        "stock": 15,
        "author": "George Orwell",  # QUE: Agregados campos: author, publication_year, isbn, condition.
        # PARA: Hacer relevante a libros usados.
        # IMPACTO: Enriquecen modelo; requieren cambios en schemas/filtros.
        "publication_year": 1949,
        "isbn": "978-0451524935",
        "condition": "bueno",
        "created_at": datetime(2024, 1, 15, 9, 0, 0)
    },
    2: {
        "id": 2,
        "name": "El Gran Gatsby",
        "description": "Novela de F. Scott Fitzgerald",
        "price": 9.99,
        "genre_id": 1,
        "stock": 20,
        "author": "F. Scott Fitzgerald",
        "publication_year": 1925,
        "isbn": "978-0743273565",
        "condition": "regular",
        "created_at": datetime(2024, 2, 1, 10, 0, 0)
    },
    # ... (agrega más ejemplos similares si quieres)
}
next_book_id = 9  # QUE: Cambiado next_product_id a next_book_id.
# PARA: Consistencia.
# IMPACTO: Afecta IDs nuevos.

# ============================================
# HELPER FUNCTIONS
# ============================================
def get_next_genre_id() -> int:  # QUE: Cambiado nombre de función.
    # PARA: Adaptar.
    # IMPACTO: Usado en routers.
    """Obtener y incrementar ID de género"""
    global next_genre_id
    current = next_genre_id
    next_genre_id += 1
    return current

def get_next_book_id() -> int:  # QUE: Cambiado nombre.
    # PARA: Adaptar.
    # IMPACTO: Usado en routers.
    """Obtener y incrementar ID de libro"""
    global next_book_id
    current = next_book_id
    next_book_id += 1
    return current