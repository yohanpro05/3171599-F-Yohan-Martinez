"""
Simulación de Base de Datos
===========================

Base de datos en memoria para el proyecto de gestión de libros usados.
"""

# "Base de datos" en memoria: {id: libro_dict}
books_db: dict[int, dict] = {}

# Contador para IDs autoincrementales
_id_counter = 0


def get_next_id() -> int:
    """Obtener el siguiente ID disponible."""
    global _id_counter
    _id_counter += 1
    return _id_counter


def find_by_isbn(isbn: str) -> dict | None:
    """Buscar un libro por su ISBN (insensible a mayúsculas)."""
    if not isbn:
        return None
    
    isbn_clean = isbn.replace("-", "").upper()  # quitamos guiones y normalizamos
    for book in books_db.values():
        if book.get("isbn"):
            if book["isbn"].replace("-", "").upper() == isbn_clean:
                return book
    return None


def reset_db() -> None:
    """Resetear base de datos (útil para tests)."""
    global _id_counter
    books_db.clear()
    _id_counter = 0