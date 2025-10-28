from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_individual_without_body(client: AsyncClient) -> None:
    res = await client.post("/bases/1/individuals")
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_create_individual(client: AsyncClient) -> None:
    res = await client.post(
        "/bases/1/individuals",
        json={
            "first_name": "John",
            "last_name": "Doe",
        },
    )
    assert res.status_code == 201
    assert res.json() == {"individual_id": 1}


@pytest.mark.asyncio
async def test_get_individual(client: AsyncClient) -> None:
    res = await client.get("/bases/1/individuals/1")
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_delete_individual(client: AsyncClient) -> None:
    res = await client.delete("/bases/1/individuals/1")
    assert res.status_code == 200
    assert res.json() == {"success": True, "message": "Individual deleted successfully"}
