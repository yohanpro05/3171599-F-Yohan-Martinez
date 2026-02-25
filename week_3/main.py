"""
API de E-commerce de Libros Usados - Main
=========================================
Punto de entrada de la aplicación.
# QUE: Cambiado título y descripción.
# PARA: Adaptar al dominio.
# IMPACTO: Actualiza metadata en docs.
"""
from fastapi import FastAPI
from routers import categories, products  # QUE: Sin cambio, pero routers internos se adaptaron.
# PARA: Mantener inclusión.
# IMPACTO: Routers ahora son para genres y books.
app = FastAPI(
    title="API de E-commerce de Libros Usados",
    description="API completa con CRUD para géneros y libros usados, con filtrado, paginación y ordenamiento",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
# Incluir routers
app.include_router(categories.router)  # Ahora es genres
app.include_router(products.router)  # Ahora es books

@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz"""
    return {
        "message": "API de E-commerce de Libros Usados",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health", tags=["Root"])
async def health_check():
    """Health check"""
    return {"status": "healthy"}