# Libros Usados API - Semana 04

API REST desarrollada con **FastAPI** para la gestión de anuncios de **libros usados** (e-commerce de segunda mano). Proyecto correspondiente a la Semana 04 del bootcamp.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128+-green)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![uv](https://img.shields.io/badge/uv-dependency%20manager-orange)

## Descripción

Esta API permite:
- Publicar anuncios de libros usados en venta
- Listar y filtrar anuncios por estado, condición física y precio máximo
- Gestionar el estado de los anuncios (available → reserved → sold / cancelled)
- Obtener estadísticas básicas del catálogo
- Manejo consistente de errores con códigos y mensajes personalizados

Todo el proyecto está adaptado al dominio **e-commerce de libros usados**, con estados y transiciones de negocio coherentes.

## Tecnologías utilizadas

- **Framework**: FastAPI
- **Validación y serialización**: Pydantic
- **Gestión de dependencias**: uv
- **Base de datos**: In-memory (simulada con diccionario)
- **Contenerización**: Docker + Docker Compose
- **Documentación automática**: OpenAPI / Swagger UI

## Instalación y ejecución local

### Requisitos

- Python 3.12+
- uv (recomendado)
- Docker + Docker Compose (opcional)

### Pasos

1. Clonar el repositorio

```bash
git clone <tu-repo-url>
cd <nombre-carpeta>
```

2. Crear y activar entorno virtual

```bash
uv venv
source .venv/bin/activate   # Linux/Mac
# o en Windows: .venv\Scripts\activate
```

3. Instalar dependencias

```bash
uv sync
```

4. Ejecutar la API (modo desarrollo)

```bash
uv run uvicorn main:app --reload
```

### Accede a:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Con Docker

```bash
docker compose up --build
```

Accede a http://localhost:8000/docs (o el puerto configurado en docker-compose.yml)

# Endpoints principales

|Método|Ruta  |Descripción                              |
|------|------|-----------------------------------------|
GET    |/listings |Listar anuncios (con filtros y paginación)
GET|/listings/{listing_id}|Obtener detalle de un anuncio|
POST|/listings|Crear nuevo anuncio|
PUT|/listings/{listing_id}|Actualizar completamente un anuncio|
PATCH|/listings/{listing_id}/status|Cambiar estado del anuncio|
DELETE|/listings/{listing_id}|Eliminar un anuncio|
GET|/listings/stats|Estadísticas del catálogo|
GET|/health|Health check del servicio|

# Estados del anuncio y transiciones válidas

```text
available ──► reserved ──► sold
   │             │
   └─────────────┴───────► cancelled
```

Transiciones permitidas:

- available → reserved / cancelled
- reserved → sold / cancelled
- No se permiten retrocesos (sold/cancelled no vuelven a estados anteriores)

# Autor

Yohan
Bootcamp FastAPI - Semana 04
Bogotá, Colombia - Marzo 2026
¡Gracias por revisar! 🚀
