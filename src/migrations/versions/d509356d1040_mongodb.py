"""mongodb

Revision ID: d509356d1040
Revises: e175833fd6f3
Create Date: 2024-11-26 09:39:27.521132

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pymongo import MongoClient, ASCENDING, DESCENDING


# revision identifiers, used by Alembic.
revision: str = "d509356d1040"
down_revision: Union[str, None] = "e175833fd6f3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

client = MongoClient("mongodb://mongodb:abcd1234@localhost:27017/")
db = client["deep_brain"]

def upgrade() -> None:
    # nodes
    db["nodes"].create_index([("label", ASCENDING)], unique=True)

    # relations
    db["relations"].create_index([("from_node", 1), ("to_node", 1)], unique=True)


def downgrade() -> None:
    # nodes
    db["nodes"].drop_index([("label", ASCENDING)])

    # relations
    db["relations"].drop_index([("from_node", 1), ("to_node", 1)])
