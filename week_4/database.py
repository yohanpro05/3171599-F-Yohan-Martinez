"""
Task Manager API - Simulación de Base de Datos
Semana 04 - Proyecto

Base de datos en memoria para el proyecto.
"""

"""
QUE:    Simula una base de datos en memoria (in-memory) para almacenar los anuncios de libros usados durante el desarrollo y pruebas. Incluye inicialización con datos de ejemplo.
PARA:   Permitir pruebas rápidas sin necesidad de PostgreSQL/MySQL/etc., mantener el estado de los anuncios entre peticiones (mientras el servidor está corriendo), y proporcionar datos iniciales para demostrar la funcionalidad de la API en /docs.
IMPACTO: Si está bien implementado → desarrollo ágil, pruebas fáciles, datos de ejemplo coherentes con el dominio y buena demostración en Swagger / Si no se adapta o tiene errores → datos inconsistentes, endpoints que fallan por falta de datos, o confusión en la evaluación al no reflejar el dominio real.
"""

from datetime import datetime, timezone

from models import ListingStatus, BookCondition


# Simulated database (in-memory)
listings_db: dict[int, dict] = {}
listing_id_counter: int = 0


def get_next_id() -> int:
    """Genera el siguiente ID para un anuncio"""
    global listing_id_counter
    listing_id_counter += 1
    return listing_id_counter


def seed_database() -> None:
    """Inicializa la base de datos con anuncios de ejemplo de libros usados"""
    global listings_db, listing_id_counter
    
    sample_listings = [
        {
            "title": "Cien años de soledad",
            "author": "Gabriel García Márquez",
            "isbn": "9788437604947",
            "publication_year": 1967,
            "price": 45000.0,
            "condition": BookCondition.VERY_GOOD,
            "description": "Edición de bolsillo, buen estado general, páginas levemente amarillentas.",
            "status": ListingStatus.AVAILABLE,
        },
        {
            "title": "El amor en los tiempos del cólera",
            "author": "Gabriel García Márquez",
            "isbn": "9780307389732",
            "publication_year": 1985,
            "price": 38000.0,
            "condition": BookCondition.GOOD,
            "description": "Tapa blanda, algunas marcas de uso, pero interior limpio.",
            "status": ListingStatus.RESERVED,
        },
        {
            "title": "1984",
            "author": "George Orwell",
            "isbn": "9780451524935",
            "publication_year": 1949,
            "price": 32000.0,
            "condition": BookCondition.FAIR,
            "description": "Edición antigua, tapa desgastada, pero texto legible.",
            "status": ListingStatus.AVAILABLE,
        },
        {
            "title": "Harry Potter y la piedra filosofal",
            "author": "J.K. Rowling",
            "isbn": "9788478884452",
            "publication_year": 1997,
            "price": 55000.0,
            "condition": BookCondition.EXCELLENT,
            "description": "Edición ilustrada, como nuevo, sin marcas.",
            "status": ListingStatus.SOLD,
        },
    ]
    
    for listing_data in sample_listings:
        listing_id = get_next_id()
        now = datetime.now(timezone.utc)
        
        listings_db[listing_id] = {
            "id": listing_id,
            "title": listing_data["title"],
            "author": listing_data["author"],
            "isbn": listing_data.get("isbn"),
            "publication_year": listing_data.get("publication_year"),
            "price": listing_data["price"],
            "condition": listing_data["condition"],
            "description": listing_data.get("description"),
            "status": listing_data["status"],
            "created_at": now,
            "updated_at": None,
            "reserved_at": now if listing_data["status"] == ListingStatus.RESERVED else None,
            "sold_at": now if listing_data["status"] == ListingStatus.SOLD else None,
        }


# Inicializar con datos de ejemplo
seed_database()
