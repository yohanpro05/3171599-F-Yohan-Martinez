# API de Gestión de Libros Usados - Proyecto Semana 02

API REST desarrollada con **FastAPI** y **Pydantic v2** para gestionar un catálogo de libros de segunda mano.  
Proyecto realizado como parte de la Semana 02 del curso [nombre del curso si aplica].

## Tecnologías utilizadas

- Python 3.10+
- FastAPI (framework web)
- Pydantic v2 (validación y serialización de datos)
- Docker + Docker Compose (para entorno reproducible)
- Base de datos en memoria (simulación simple para el ejercicio)

## Características principales

- CRUD completo de libros
- Validación y normalización automática de datos:
  - Títulos y autores capitalizados
  - Géneros en minúsculas, sin duplicados y límite de 8
  - ISBN validado (10 o 13 dígitos)
- Paginación en el listado de libros
- Filtro por libros destacados (`is_featured`)
- Alternar estado de destacado
- Manejo de errores con códigos HTTP apropiados (404, 409, 400, etc.)

## Endpoints principales

| Método | Ruta                          | Descripción                          | Tags     |
|--------|-------------------------------|--------------------------------------|----------|
| POST   | `/books`                      | Crear un nuevo libro                 | Books    |
| GET    | `/books`                      | Listar libros (con paginación)       | Books    |
| GET    | `/books/{book_id}`            | Obtener detalles de un libro         | Books    |
| PATCH  | `/books/{book_id}`            | Actualizar libro parcialmente        | Books    |
| DELETE | `/books/{book_id}`            | Eliminar un libro                    | Books    |
| POST   | `/books/{book_id}/featured`   | Alternar estado de destacado         | Books    |
| GET    | `/`                           | Health check de la API               | Health   |

Documentación interactiva (Swagger):  
http://localhost:8000/docs (una vez que la API esté corriendo)

## Cómo ejecutar el proyecto

### Requisitos

- Docker y Docker Compose instalados (recomendado)
- O bien: Python 3.10+, `pip` y `uvicorn`

### Con Docker (recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/NOMBRE_DEL_REPO.git
cd NOMBRE_DEL_REPO

# Levantar la API
docker compose up --build

Opción 2: Ejecución local (sin Docker)

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la API
uvicorn main:app --reload --port 8000

Ejemplo de creación de libro (POST /books)
Body JSON de ejemplo:
JSON{
  "title": "Cien años de soledad",
  "author": "Gabriel García Márquez",
  "isbn": "9788437604947",
  "publisher": "Penguin Random House",
  "publication_year": 1967,
  "condition": "good",
  "price": 45000.0,
  "currency": "COP",
  "stock": 3,
  "description": "Edición clásica en buen estado, con leves marcas de uso.",
  "genres": ["Novela", "Realismo mágico", "Clásico colombiano"],
  "is_featured": true
}
Respuesta esperada (ejemplo):
JSON{
  "id": 1,
  "title": "Cien Años De Soledad",
  "author": "Gabriel García Márquez",
  "isbn": "9788437604947",
  ...
  "created_at": "2025-02-18T02:30:00",
  "updated_at": null
}

```
Estructura del proyecto
.
├── main.py               # Archivo principal de FastAPI
├── schemas.py            # Modelos Pydantic (BookBase, BookCreate, etc.)
├── database.py           # Simulación de base de datos en memoria
├── requirements.txt      # Dependencias del proyecto
├── Dockerfile            # (si lo tienes)
├── docker-compose.yml    # Configuración de Docker
└── README.md             # Este archivo




Autor
Yohan
Bogotá D.C., Colombia
GitHub | LinkedIn