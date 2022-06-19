from fastapi import APIRouter

from app.api.endpoints import shop_unit, api_stats


api_router = APIRouter()
api_router.include_router(shop_unit.router, tags=["shop_unit_operations"])
api_router.include_router(api_stats.router, tags=["shop_unit_stat"])