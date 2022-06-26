from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from fastapi import APIRouter, Query

from app.schema.response import ShopUnitStatisticResponse, ShopUnitNode
from app.schema.schemas import Error, ShopUnitType

router = APIRouter()


@router.get(
    "/node/{id}/statistic",
    response_model=ShopUnitStatisticResponse,
    responses={"400": {"model": Error}, "404": {"model": Error}},
)
async def get_node_id_statistic(
    id: UUID,
    date_start: Optional[datetime] = Query(None, alias="dateStart"),
    date_end: Optional[datetime] = Query(None, alias="dateEnd"),
) -> Union[ShopUnitStatisticResponse, Error]:
    pass




@router.get(
    "/sales",
    response_model=ShopUnitStatisticResponse,
    responses={"400": {"model": Error}},
)
async def get_sales(date: datetime) -> Union[ShopUnitStatisticResponse, Error]:
    pass
