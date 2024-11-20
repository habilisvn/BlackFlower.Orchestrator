# from uuid import uuid4
from mongoengine import Document, StringField


class Node(Document):
    # id = StringField(primary_key=True, default=lambda: str(uuid4()))
    label = StringField(unique=True, required=True)
