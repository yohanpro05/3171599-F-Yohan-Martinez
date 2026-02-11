# API de Bienvenida - E-commerce de Libros Usados

Proyecto Semana 01 - Bootcamp FastAPI

API simple que simula una bienvenida personalizada a una tienda de libros usados, con mensajes según estilo y hora del día, más info básica de libros.

## Endpoints principales

- `GET /` → Información general de la API  
- `GET /welcome/{name}` → Bienvenida personalizada (ej: ?style=formal)  
- `GET /book-info/{title}` → Información simulada de un libro usado (ej: ?author=Orwell)  
- `GET /welcome/{name}/time-based` → Mensaje según la hora (?hour=10)  
- `GET /health` → Health check de la API

## Cómo ejecutar

### Local (con uv)

```bash
uv sync --frozen --no-dev
uv run uvicorn src.main:app --reload
# con docker 
docker compose up --build

Accede a la documentación interactiva en:
http://localhost:8000/docs
Tecnologías

FastAPI
Uvicorn
Python 3.11+
UV (gestor de dependencias)

Proyecto realizado en el bootcamp FastAPI Zero to Hero – Semana 01
Autor: Yohan