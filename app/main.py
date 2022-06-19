
from __future__ import annotations

from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from fastapi import FastAPI, Query

from app.schemas.schemas import Error, ShopUnit, ShopUnitImportRequest, ShopUnitStatisticResponse

app = FastAPI(
    description='Вступительное задание в Летнюю Школу Бэкенд Разработки Яндекса 2022',
    title='Mega Market Open API',
    version='1.0',
)

