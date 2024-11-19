from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, Query
from pydantic import UUID4

from nodes.infra.repository import NodeRepository
from nodes.repr.dependencies import (
    get_node_repository,
)
from nodes.repr.validations import NodeOut
from user.repr.dependencies import get_current_user


router = APIRouter(
    prefix="/v1/nodes", tags=["node"], dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=dict[str, list[NodeOut] | int])
async def get_nodes(
    *,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
    node_repo: Annotated[NodeRepository, Depends(get_node_repository)],
):
    offset = (page - 1) * page_size
    result = await node_repo.find_all(limit=page_size, offset=offset)

    return {"data": result, "page": page, "page_size": page_size}


@router.get("/{node_id}", response_model=NodeOut)
async def get_node(
    node_id: UUID4,
    node_repo: Annotated[NodeRepository, Depends(get_node_repository)]
):
    result = await node_repo.find_by_id(entity_id=node_id)
    if not result:
        raise HTTPException(status_code=404, detail="Node not found")
    return result
