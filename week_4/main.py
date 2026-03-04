"""
QUE:    Punto de entrada principal de la API FastAPI. Define la aplicación, configura metadata (título, descripción, tags, etc.), registra handlers de excepciones, funciones helper y todos los endpoints de la API.
PARA:   Servir como el núcleo central que une todos los componentes del proyecto (modelos, base de datos in-memory, excepciones, rutas). Es el archivo que FastAPI ejecuta primero y el que genera la documentación automática en /docs.
IMPACTO: Si está bien estructurado y documentado → excelente experiencia de desarrollo y documentación clara / Si tiene errores o falta metadata → documentación pobre, endpoints confusos, manejo de errores inconsistente y dificultad para depurar.
"""

from datetime import datetime, timezone
from typing import Annotated, List

from fastapi import FastAPI, Path, Query, status

from models import (
    ListingStatus,
    BookCondition,
    ListingCreate,
    ListingUpdate,
    StatusUpdate,
    ListingResponse,
    ListingListResponse,
    ListingStats,
    ErrorResponse,
)
from database import listings_db, get_next_id
from exceptions import (
    ListingException,
    ListingNotFoundError,
    InvalidStatusTransitionError,
    DuplicateListingError,
    listing_exception_handler,
)


# ============================================
# CONFIGURACIÓN DE LA APP
# ============================================

tags_metadata = [
    {
        "name": "listings",
        "description": "Operaciones CRUD sobre anuncios de libros usados"
    },
    {
        "name": "stats",
        "description": "Estadísticas generales del catálogo"
    },
    {
        "name": "health",
        "description": "Verificación del estado del servicio"
    },
]

app = FastAPI(
    title="Used Books Marketplace API",
    description="""
    API REST para la gestión de **anuncios de libros usados**.

    Funcionalidades principales:
    - Publicar libros usados en venta
    - Buscar y filtrar anuncios por estado, condición, precio máximo
    - Gestionar el estado del anuncio (available → reserved → sold)
    - Estadísticas básicas del catálogo
    """,
    version="1.0.0",
    contact={
        "name": "Yohan - Bootcamp FastAPI",
        "url": "https://github.com/tu-usuario",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ============================================
# MANEJADORES DE EXCEPCIONES
# ============================================

app.add_exception_handler(ListingException, listing_exception_handler)


# ============================================
# FUNCIONES HELPER
# ============================================

def validate_status_transition(current: ListingStatus, target: ListingStatus) -> bool:
    """
    Reglas de transición de estado para anuncios de libros usados:
    - available   → reserved   OK
    - available   → cancelled  OK
    - reserved    → sold       OK
    - reserved    → cancelled  OK
    - sold        → cualquier  NO
    - cancelled   → cualquier  NO
    """
    allowed = {
        ListingStatus.AVAILABLE: [ListingStatus.RESERVED, ListingStatus.CANCELLED],
        ListingStatus.RESERVED:  [ListingStatus.SOLD, ListingStatus.CANCELLED],
        ListingStatus.SOLD:      [],
        ListingStatus.CANCELLED: [],
    }
    return target in allowed.get(current, [])


def check_duplicate_listing(title: str, author: str, exclude_id: int | None = None) -> bool:
    """Verifica si ya existe un anuncio con el mismo título y autor"""
    for listing_id, listing in listings_db.items():
        if (
            listing["title"].lower() == title.lower()
            and listing["author"].lower() == author.lower()
        ):
            if exclude_id is None or listing_id != exclude_id:
                return True
    return False


# ============================================
# ENDPOINTS
# ============================================

@app.get(
    "/listings",
    response_model=ListingListResponse,
    tags=["listings"],
    summary="Listar anuncios de libros usados",
    description="Devuelve una lista paginada de anuncios con filtros opcionales por estado, condición y precio máximo",
    responses={
        200: {"model": ListingListResponse},
        422: {"model": ErrorResponse},
    }
)
async def list_listings(
    status: Annotated[ListingStatus | None, Query(description="Filtrar por estado del anuncio")] = None,
    condition: Annotated[BookCondition | None, Query(description="Filtrar por condición física del libro")] = None,
    max_price: Annotated[float | None, Query(gt=0, description="Precio máximo en COP")] = None,
    skip: Annotated[int, Query(ge=0, description="Offset para paginación")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Límite de resultados")] = 20,
):
    filtered = list(listings_db.values())

    if status:
        filtered = [l for l in filtered if l["status"] == status]
    if condition:
        filtered = [l for l in filtered if l["condition"] == condition]
    if max_price:
        filtered = [l for l in filtered if l["price"] <= max_price]

    total = len(filtered)
    paginated = filtered[skip : skip + limit]

    return ListingListResponse(
        items=[ListingResponse(**l) for l in paginated],
        total=total,
        skip=skip,
        limit=limit
    )


@app.get(
    "/listings/{listing_id}",
    response_model=ListingResponse,
    tags=["listings"],
    summary="Obtener detalle de un anuncio específico",
    responses={
        200: {"model": ListingResponse},
        404: {"model": ErrorResponse},
    }
)
async def get_listing(
    listing_id: Annotated[int, Path(ge=1, description="ID del anuncio")]
):
    if listing_id not in listings_db:
        raise ListingNotFoundError(listing_id)
    
    return ListingResponse(**listings_db[listing_id])


@app.post(
    "/listings",
    status_code=status.HTTP_201_CREATED,
    response_model=ListingResponse,
    tags=["listings"],
    summary="Crear un nuevo anuncio de libro usado",
    responses={
        201: {"model": ListingResponse},
        409: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    }
)
async def create_listing(listing: ListingCreate):
    if check_duplicate_listing(listing.title, listing.author):
        raise DuplicateListingError(listing.title, listing.author)

    now = datetime.now(timezone.utc)
    new_id = get_next_id()
    
    data = listing.model_dump()
    data.update({
        "id": new_id,
        "status": ListingStatus.AVAILABLE,
        "created_at": now,
        "updated_at": now,
        "reserved_at": None,
        "sold_at": None,
    })
    
    listings_db[new_id] = data
    return ListingResponse(**data)


@app.patch(
    "/listings/{listing_id}/status",
    response_model=ListingResponse,
    tags=["listings"],
    summary="Actualizar el estado de un anuncio",
    description="Permite cambiar el estado siguiendo reglas de negocio (available → reserved → sold, etc.)",
    responses={
        200: {"model": ListingResponse},
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    }
)
async def update_listing_status(
    listing_id: Annotated[int, Path(ge=1, description="ID del anuncio")],
    status_update: StatusUpdate
):
    if listing_id not in listings_db:
        raise ListingNotFoundError(listing_id)
    
    current = listings_db[listing_id]
    current_status = current["status"]
    new_status = status_update.status

    if not validate_status_transition(current_status, new_status):
        raise InvalidStatusTransitionError(current_status, new_status)

    now = datetime.now(timezone.utc)
    update_data = {"status": new_status, "updated_at": now}

    if new_status == ListingStatus.RESERVED:
        update_data["reserved_at"] = now
    elif new_status == ListingStatus.SOLD:
        update_data["sold_at"] = now

    current.update(update_data)
    listings_db[listing_id] = current

    return ListingResponse(**current)


@app.get(
    "/listings/stats",
    response_model=ListingStats,
    tags=["stats"],
    summary="Obtener estadísticas generales del catálogo",
    responses={200: {"model": ListingStats}}
)
async def get_stats():
    if not listings_db:
        return ListingStats(
            total_listings=0,
            by_status={},
            average_price=0.0,
            max_price=0.0
        )

    total = len(listings_db)
    by_status = {}
    prices = []

    for listing in listings_db.values():
        st = listing["status"]
        by_status[st.value] = by_status.get(st.value, 0) + 1
        prices.append(listing["price"])

    avg_price = sum(prices) / total if prices else 0
    max_p = max(prices) if prices else 0

    return ListingStats(
        total_listings=total,
        by_status=by_status,
        average_price=round(avg_price, 2),
        max_price=max_p
    )


# ============================================
# HEALTH CHECK
# ============================================

@app.get(
    "/health",
    tags=["health"],
    summary="Health check del servicio",
    response_description="Confirma que la API está operativa"
)
async def health_check():
    """Endpoint simple para verificar que el servicio está corriendo correctamente."""
    return {
        "status": "healthy",
        "service": "used-books-api",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }