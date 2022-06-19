from fastapi import APIRouter, FastAPI, Query


from typing import Union, Optional
from datetime import datetime
from uuid import UUID

from app.schemas.schemas import (
    ShopUnit,
    ShopUnitStatisticResponse,
    Error)


router = APIRouter()

@router.get(
    '/node/{id}/statistic',
    response_model=ShopUnitStatisticResponse,
    responses={'400': {'model': Error}, '404': {'model': Error}},
)
def get_node_id_statistic(
    id: UUID,
    date_start: Optional[datetime] = Query(None, alias='dateStart'),
    date_end: Optional[datetime] = Query(None, alias='dateEnd'),
) -> Union[ShopUnitStatisticResponse, Error]:
    pass


@router.get(
    '/nodes/{id}',
    response_model=ShopUnit,
    responses={'400': {'model': Error}, '404': {'model': Error}},
)
def get_nodes_id(id: UUID) -> Union[ShopUnit, Error]:
    pass

@router.get(
    '/sales',
    response_model=ShopUnitStatisticResponse,
    responses={'400': {'model': Error}},
)
def get_sales(date: datetime) -> Union[ShopUnitStatisticResponse, Error]:
    pass
