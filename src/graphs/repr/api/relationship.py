from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, Query

from graphs.domain import RelationshipEntity
from graphs.infra.repository import RelationshipRepository
from graphs.repr.dependencies import (
    get_relationship_repository,
    validate_nodes_exist,
    validate_relationship_exists,
)
from graphs.repr.validations import RelationshipOut, RelationshipCreateIn
from user.repr.dependencies import get_current_user


router = APIRouter(
    prefix="/v1/relationships",
    tags=["relationship"],
    dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=dict[str, list[RelationshipOut] | int])
async def get_relationships(
    *,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
    relationship_repo: Annotated[RelationshipRepository, Depends(get_relationship_repository)],
):
    offset = (page - 1) * page_size
    result = await relationship_repo.find_all(limit=page_size, offset=offset)
    return {"data": result, "page": page, "page_size": page_size}


@router.get("/node/{node_label}")
async def get_node_relationships(
    node_label: str,
    relationship_repo: Annotated[RelationshipRepository, Depends(get_relationship_repository)]
):
    result = await relationship_repo.find_by_node_label(node_label=node_label)
    return result


@router.post(
    "",
    status_code=201,
    dependencies=[
        Depends(validate_nodes_exist),
        Depends(validate_relationship_exists),
    ]
)
async def create_relationship(
    relationship: RelationshipCreateIn,
    relationship_repo: Annotated[RelationshipRepository, Depends(get_relationship_repository)],
) -> dict[str, str]:
    relationship_entity = RelationshipEntity.model_validate(relationship)
    await relationship_repo.save(relationship_entity)
    return {"message": "Relationship created successfully"}


@router.delete("/{from_node}/{to_node}", status_code=204)
async def delete_relationship(
    from_node: str,
    to_node: str,
    relationship_repo: Annotated[RelationshipRepository, Depends(get_relationship_repository)],
):
    # Check if relationship exists
    existing = await relationship_repo.find_relationship(from_node, to_node)
    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")
    
    await relationship_repo.delete(from_node, to_node)
    return None 