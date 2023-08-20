from fastapi import APIRouter

from .favorites import router as favorites_router
from .films import router as films_router
from .status import router as status_router
from .views import router as views_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(status_router)
v1_router.include_router(views_router)
v1_router.include_router(favorites_router)
v1_router.include_router(films_router)
