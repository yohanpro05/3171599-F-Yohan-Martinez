"""
Task Manager API - Excepciones Personalizadas
Semana 04 - Proyecto

Define excepciones de negocio y handlers.
"""

"""
QUE:    Define las excepciones personalizadas del proyecto y el handler global para manejarlas de forma consistente en toda la API.
PARA:   Proporcionar errores HTTP bien estructurados y con mensajes claros (código, mensaje, detalles), mejorar la experiencia del usuario y facilitar la depuración. El handler asegura que todas las excepciones personalizadas devuelvan el mismo formato JSON en las respuestas de error.
IMPACTO: Si está bien implementado → manejo de errores profesional, documentación clara en Swagger (con ejemplos de errores), respuestas consistentes (400, 404, 409) y buena puntuación en "Manejo de errores consistente" (10 puntos) / Si está incompleto o inconsistente → respuestas genéricas de FastAPI, errores confusos para el cliente y baja nota en calidad del código.
"""

from fastapi import Request
from fastapi.responses import JSONResponse


# ============================================
# EXCEPCIONES PERSONALIZADAS
# ============================================

class ListingException(Exception):
    """
    Excepción base para la API de anuncios de libros usados.
    
    Contiene:
    - code: str (código único del error)
    - message: str (mensaje descriptivo)
    - status_code: int (código HTTP)
    - details: dict | None (detalles adicionales)
    """
    
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: dict | None = None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class ListingNotFoundError(ListingException):
    """
    Excepción cuando un anuncio no se encuentra.
    """
    
    def __init__(self, listing_id: int):
        super().__init__(
            code="LISTING_NOT_FOUND",
            message=f"Anuncio con id {listing_id} no encontrado",
            status_code=404
        )


class InvalidStatusTransitionError(ListingException):
    """
    Excepción cuando se intenta una transición de estado inválida.
    """
    
    def __init__(self, current_status: str, target_status: str):
        super().__init__(
            code="INVALID_STATUS_TRANSITION",
            message=f"Transición inválida de '{current_status}' a '{target_status}'",
            status_code=400
        )


class DuplicateListingError(ListingException):
    """
    Excepción cuando se intenta crear un anuncio duplicado (mismo título y autor).
    """
    
    def __init__(self, title: str, author: str):
        super().__init__(
            code="DUPLICATE_LISTING",
            message=f"Ya existe un anuncio con título '{title}' del autor '{author}'",
            status_code=409
        )


# ============================================
# MANEJADOR DE EXCEPCIONES
# ============================================

async def listing_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, ListingException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details
                }
            }
        )
    # Opcional: manejar otros errores
    return JSONResponse(status_code=500, content={"detail": "Error interno"})