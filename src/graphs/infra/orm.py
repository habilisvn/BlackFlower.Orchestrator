from mongoengine import StringField, ReferenceField

from common.base import BaseDocument


class Node(BaseDocument):
    label = StringField(unique=True, required=True)


class Relation(BaseDocument):
    from_node = ReferenceField(Node, required=True)
    to_node = ReferenceField(Node, required=True)
