import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestImports:
    async def test_common_case(self, client: AsyncClient, setup_db):

        response = await client.post(
            url="/imports",
            json={
                "items": [
                    {
                        "type": "CATEGORY",
                        "name": "Товары",
                        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                        "parentId": None,
                    }
                ],
                "updateDate": "2022-02-01T12:00:00.000Z",
            },
        )
        assert response.status_code == 200
