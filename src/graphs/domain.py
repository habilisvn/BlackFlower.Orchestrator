from typing import Any, NewType

from pydantic import ConfigDict, Field

from common.base import BaseEntity


Label = NewType('Label', str)


class RelationshipEntity(BaseEntity):
    from_node: Label
    to_node: Label
    relation_type: str


class NodeEntity(BaseEntity):
    # DOCUMENT: exclude _id from entity (default primary key of MongoDB)
    id: Any = Field(exclude=True, alias="_id", default=None)
    label: Label
    relationships: list[RelationshipEntity | None] = []

    model_config = ConfigDict(extra="allow")

    def add_relationship(self, relationship: 'NodeEntity'):
        rel = RelationshipEntity(
            from_node_id=self.id,
            to_node_id=relationship.id
        )
        self.relationships.append(rel)
        relationship.relationships.append(rel)
