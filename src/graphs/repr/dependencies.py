from typing import Annotated
from fastapi import Depends, HTTPException

from graphs.infra.repository import NodeRepository, RelationshipRepository
from common.dependencies import MongoDBDpd
from graphs.repr.validations import NodeCreateIn, RelationshipCreateIn


async def get_node_repository(db: MongoDBDpd) -> NodeRepository:
    return NodeRepository(db)


async def get_relationship_repository(
    db: MongoDBDpd
) -> RelationshipRepository:
    return RelationshipRepository(db)


async def validate_label_exists(
    node: NodeCreateIn,
    node_repo: Annotated[NodeRepository, Depends(get_node_repository)]
) -> None:
    if await node_repo.find_by_label(node.label):
        raise HTTPException(status_code=400, detail="Node already exists")


async def validate_nodes_exist(
    relationship: RelationshipCreateIn,
    node_repo: Annotated[NodeRepository, Depends(get_node_repository)]
) -> None:
    # Check if from_node exists
    from_node = await node_repo.find_by_label(relationship.from_node)
    if not from_node:
        raise HTTPException(status_code=404, detail="From node not found")
    
    # Check if to_node exists
    to_node = await node_repo.find_by_label(relationship.to_node)
    if not to_node:
        raise HTTPException(status_code=404, detail="To node not found")


async def validate_relationship_exists(
    relationship: RelationshipCreateIn,
    relationship_repo: Annotated[RelationshipRepository, Depends(get_relationship_repository)]
) -> None:
    # Check if relationship already exists
    existing = await relationship_repo.find_relationship(
        relationship.from_node,
        relationship.to_node
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Relationship between these nodes already exists"
        )
