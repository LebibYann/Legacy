from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_family(client: AsyncClient) -> None:
    res = await client.post("/family", json={"name": "Doe", "members": []})
    assert res.status_code == 201
    assert res.json() == {"id": 1, "name": "Doe", "members": []}
