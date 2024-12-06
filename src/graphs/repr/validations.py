from pydantic import BaseModel, ConfigDict


class RelationshipBase(BaseModel):
    from_node: str
    to_node: str
    relation_type: str


class RelationshipCreateIn(RelationshipBase):
    pass


class RelationshipOut(RelationshipBase):
    pass


class NodeRelationship(BaseModel):
    to_node: str
    relationship_type: str


class NodeBase(BaseModel):
    label: str
    relationships: list[NodeRelationship | None] = []

    model_config = ConfigDict(extra="allow")


class NodeCreateIn(NodeBase):
    pass


class NodeOut(NodeBase):
    pass
