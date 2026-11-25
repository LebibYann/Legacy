from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_base(client: AsyncClient) -> None:
    res = await client.post("/bases", json={"name": "Doe"})
    assert res.status_code == 201
    assert res.json() == {"base_id": 1, "name": "Doe"}


@pytest.mark.asyncio
async def test_list_bases(client: AsyncClient) -> None:
    res = await client.get("/bases")
    assert res.status_code == 200
