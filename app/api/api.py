from fastapi import APIRouter

from app.api.endpoints import api_stats, api_unit

api_router = APIRouter()
api_router.include_router(api_unit.router, tags=["Base"])
api_router.include_router(api_stats.router, tags=["Stat"])
