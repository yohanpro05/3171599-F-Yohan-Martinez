# API de E-commerce de Libros Usados

API REST con FastAPI para catálogo de libros usados.  
Incluye CRUD completo para géneros y libros, con filtros, paginación y ordenamiento.

Proyecto - Semana 3 del bootcamp de FastAPI.

## Características

- CRUD géneros (géneros de libros)
- CRUD libros con campos: título, autor, año, ISBN, condición, stock, precio
- Filtros avanzados: búsqueda, género, precio, stock, año, condición
- Paginación y ordenamiento
- Validaciones: género debe existir para crear/actualizar libro
- Documentación Swagger y ReDoc

## Tecnologías

- FastAPI
- Pydantic v2
- Uvicorn
- uv (gestor de dependencias)
- Docker + docker-compose
- Base de datos: en memoria (diccionarios)

## Requisitos

- Docker y Docker Compose instalados
- (Opcional) uv instalado: https://docs.astral.sh/uv/

## Cómo ejecutar (Docker)

```bash
# 1. Entrar a la carpeta
cd week_3

# 2. Construir y levantar
docker compose build
docker compose up -d

# Ver logs
docker compose logs -f

# Acceder a Swagger (probar endpoints)
http://localhost:8000/docs

# Detener
docker compose down
```

Hot-reload incluido: cambios en código se reflejan automáticamente.

## Endpoints principales

## Géneros

- GET /genres/          → Listar todos
- GET /genres/{id}      → Obtener uno
- POST /genres/         → Crear
- PUT /genres/{id}      → Actualizar completo
- DELETE /genres/{id}   → Eliminar

## Libros

- GET /books/           → Listar (con filtros: search, genre_id, min_price, max_price, in_stock, min_year, condition, sort_by, order, page, per_page)

- GET /books/{id}       → Obtener uno (incluye género)
- POST /books/          → Crear (requiere genre_id válido)
- PUT /books/{id}       → Reemplazar completo
- PATCH /books/{id}     → Actualizar parcial
- DELETE /books/{id}    → Eliminar

## Ejemplos rápidos (curl)

Crear género:

```bash
curl -X POST "http://localhost:8000/genres/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Thriller", "description": "Novelas de suspenso"}'
``` 

Crear libro (usa genre_id real):
```
curl -X POST "http://localhost:8000/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "El código Da Vinci",
    "price": 35.0,
    "author": "Dan Brown",
    "publication_year": 2003,
    "isbn": "9788495618788",
    "condition": "bueno",
    "stock": 10,
    "genre_id": 1
  }'
  ```
  
  Listar filtrado:
  ```
  curl "http://localhost:8000/books/?search=dan&min_price=20&in_stock=true"
  ```
  
## Notas

- Datos en memoria → se pierden al reiniciar
- Sin restricción al borrar género con libros
- Autor: Yohan – Bogotá, Febrero 2026