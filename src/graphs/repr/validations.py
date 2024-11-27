from pydantic import BaseModel


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


class NodeCreateIn(NodeBase):
    pass


class NodeOut(NodeBase):
    pass
