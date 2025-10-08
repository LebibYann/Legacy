from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_family_without_body(client: AsyncClient) -> None:
    res = await client.post("/bases/1/families")
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_create_family(client: AsyncClient) -> None:
    res = await client.post(
        "/bases/1/families",
        json={
            "father_id": 0,
            "mother_id": 0,
            "same_sex_couple": False,
            "children_ids": [0],
            "events_ids": [0],
            "source_family": "Ancestry.com",
            "source_individuals": "Ancestry.com",
            "comment": "Created via API",
        },
    )
    assert res.status_code == 201
    assert res.json() == {"family_id": 1}


@pytest.mark.asyncio
async def test_create_family_to_individual(client: AsyncClient) -> None:
    res = await client.post(
        "/bases/1/families/to", json={"lastname": "Doe", "individual_id": 1}
    )
    assert res.status_code == 201
    assert res.json() == {"family_id": 1, "individual_id": 1}


@pytest.mark.asyncio
async def test_update_family(client: AsyncClient) -> None:
    res = await client.put("/bases/1/families/1", json={"lastname": "Doe"})
    assert res.status_code == 200
    assert res.json() == {"family_id": 1}


@pytest.mark.asyncio
async def test_merge_families(client: AsyncClient) -> None:
    res = await client.patch(
        "/bases/1/families/merge", json={"source_family_id": 1, "target_family_id": 2}
    )
    assert res.status_code == 200
    assert res.json() == {"family_id": 2}


@pytest.mark.asyncio
async def test_get_family(client: AsyncClient) -> None:
    res = await client.get("/bases/1/families/1")
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_delete_family(client: AsyncClient) -> None:
    res = await client.delete("/bases/1/families/1")
    assert res.status_code == 200
    assert res.json() == {"success": True}
