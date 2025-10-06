from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="", tags=["open"])


class Family(BaseModel):
    id: int
    name: str
    members: list[str]


@router.post("/family", summary="Create family", response_model=Family, status_code=201)
def create_family() -> Family:
    return Family(id=1, name="Doe", members=[])
