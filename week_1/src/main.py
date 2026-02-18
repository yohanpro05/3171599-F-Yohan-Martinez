# ============================================
# PROYECTO: API DE SALUDO - Adaptado a E-commerce de Libros Usados
# ============================================
# Semana 01 - Bootcamp FastAPI Zero to Hero

from fastapi import FastAPI, Query
from typing import Dict

app = FastAPI(
    title="Libros Usados API",
    description="API de bienvenida y consultas básicas para e-commerce de libros usados",
    version="1.0.0"
)

# ============================================
# DATOS DE CONFIGURACIÓN 
# ============================================

# Mensajes de bienvenida por "idioma" o estilo de tienda
WELCOMES: Dict[str, str] = {
    "casual": "¡Bienvenid@ a nuestra tienda de libros usados, {name}! Encuentra joyas literarias a buen precio.",
    "formal": "Estimado/a {name}, le damos la más cordial bienvenida a nuestra librería de segunda mano.",
    "amigable": "¡Hola {name}! ¿Listo para llevarte un libro que cambie tu día?",
    "nocturno": "¡Buenas noches {name}! La tienda de libros usados nunca duerme... ¿qué buscas hoy?",
}

SUPPORTED_STYLES = list(WELCOMES.keys())


# ============================================
# TODO 1: CREAR LA INSTANCIA DE FASTAPI
# ============================================
# Ya está hecho arriba con el nombre adaptado al dominio


# ============================================
# TODO 2: ENDPOINT RAÍZ
# ============================================
@app.get("/")
async def root() -> Dict[str, str | list[str]]:
    """Información general de la API adaptada al e-commerce de libros usados."""
    return {
        "name": "Libros Usados API",
        "version": "1.0.0",
        "docs": "/docs",
        "styles": SUPPORTED_STYLES,
        "message": "¡Explora libros usados con historia y a precios increíbles!"
    }


# ============================================
# TODO 3: SALUDO PERSONALIZADO (bienvenida a la tienda)
# ============================================
@app.get("/welcome/{name}")
async def welcome(
    name: str,
    style: str = Query("casual", description="Estilo de bienvenida: casual, formal, amigable, nocturno")
) -> Dict[str, str]:
    """
    Da la bienvenida personalizada al usuario en la tienda de libros usados.
    Si el estilo no existe, usa 'casual' por defecto.
    """
    welcome_style = style if style in WELCOMES else "casual"
    template = WELCOMES[welcome_style]
    message = template.format(name=name)

    return {
        "welcome": message,
        "style": welcome_style,
        "name": name
    }


# ============================================
# TODO 4: INFORMACIÓN DE ENTIDAD (info básica de un libro)
# ============================================
@app.get("/book-info/{title}")
async def book_info(
    title: str,
    author: str = Query(..., description="Autor del libro")
) -> Dict[str, str]:
    """
    Muestra información básica de un libro usado (simulada).
    """
    return {
        "title": title,
        "author": author,
        "message": f"Libro usado '{title}' de {author} - ¡Disponible en nuestra tienda!",
        "condition": "Muy bueno",  # Simulado, en versión real vendría de BD
        "price_range": "25.000 - 80.000 COP"
    }


# ============================================
# TODO 5: SERVICIO SEGÚN HORARIO (saludo / mensaje según hora)
# ============================================
def get_time_message(hour: int) -> tuple[str, str]:
    """Devuelve mensaje y período según la hora."""
    if 6 <= hour < 12:
        return "¡Buenos días! La tienda de libros usados ya abrió sus puertas.", "mañana"
    elif 12 <= hour < 18:
        return "¡Buenas tardes! Es el momento perfecto para encontrar tu próximo libro.", "tarde"
    else:
        return "¡Buenas noches! Seguimos abiertos 24/7 para los amantes de la lectura.", "noche"


@app.get("/welcome/{name}/time-based")
async def welcome_time_based(
    name: str,
    hour: int = Query(..., ge=0, le=23, description="Hora actual (0-23)")
) -> Dict[str, str | int]:
    """
    Da la bienvenida según la hora del día en la tienda de libros usados.
    """
    if not 0 <= hour <= 23:
        raise ValueError("La hora debe estar entre 0 y 23")

    message, period = get_time_message(hour)
    welcome_text = f"{message} Bienvenid@ {name}."

    return {
        "welcome": welcome_text,
        "hour": hour,
        "period": period
    }


# ============================================
# TODO 6: HEALTH CHECK
# ============================================
@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Verifica el estado de la API de libros usados."""
    return {
        "status": "healthy",
        "service": "libros-usados-api",
        "version": "1.0.0"
    }