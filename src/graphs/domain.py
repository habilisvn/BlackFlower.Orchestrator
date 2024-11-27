from common.base import BaseEntity
from typing import NewType


Label = NewType('Label', str)


class RelationshipEntity(BaseEntity):
    from_node: Label
    to_node: Label
    relation_type: str


class NodeEntity(BaseEntity):
    label: Label
    relationships: list[RelationshipEntity|None] = []

    def add_relationship(self, relationship: 'NodeEntity'):
        relationship = RelationshipEntity(from_node_id=self.id, to_node_id=relationship.id)
        self.relationships.append(relationship)
        relationship.relationships.append(relationship)
