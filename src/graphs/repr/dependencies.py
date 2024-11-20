from typing import Annotated
from fastapi import Depends, HTTPException

from graphs.infra.repository import NodeRepository
from common.dependencies import PostgresDependency
from graphs.repr.validations import NodeCreateIn


async def get_node_repository(session: PostgresDependency) -> NodeRepository:
    return NodeRepository(session)


# TEMPORARY: Remove in the future
async def validate_label_exists(
    node: NodeCreateIn,
    node_repo: Annotated[NodeRepository, Depends(get_node_repository)]
) -> str:
    check = await node_repo.find_by_label(node.label)
    if check:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    return user.email
