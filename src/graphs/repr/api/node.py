from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, Query

from graphs.domain import Label, NodeEntity
from graphs.infra.repository import NodeRepository
from graphs.repr.dependencies import (
    get_node_repository,
    validate_label_exists,
    validate_label_not_exists,
)
from graphs.repr.validations import NodeOut, NodeCreateIn
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


@router.get("/{label}", response_model=None)
async def get_node(
    label: Label,
    node_repo: Annotated[NodeRepository, Depends(get_node_repository)],
) -> NodeOut | dict:
    result = await node_repo.find_by_primary_key(label=label)
    if not result:
        raise HTTPException(status_code=404, detail="Node not found")
    return result


@router.post(
    "",
    status_code=201,
    dependencies=[Depends(validate_label_exists)],
)
async def create_node(
    node: NodeCreateIn,
    node_repo: Annotated[NodeRepository, Depends(get_node_repository)],
) -> dict[str, str]:
    node_entities = NodeEntity.model_validate(node)
    await node_repo.save(node_entities, upsert=True)

    return {"message": "Node created successfully"}


@router.delete(
    "/{label}",
    status_code=204,
    dependencies=[Depends(validate_label_not_exists)],
)
async def delete_node(
    label: Label,
    node_repo: Annotated[NodeRepository, Depends(get_node_repository)],
) -> None:
    result = await node_repo.find_by_primary_key(label=label)
    if not result:
        raise HTTPException(status_code=404, detail="Node not found")

    await node_repo.delete(label)
