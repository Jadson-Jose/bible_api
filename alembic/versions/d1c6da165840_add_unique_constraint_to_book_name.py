"""add unique constraint to book name

Revision ID: d1c6da165840
Revises: e0217353303f
Create Date: 2026-02-10 08:44:37.800450

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d1c6da165840"
down_revision: Union[str, None] = "e0217353303f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("up_books_name", "books", ["name"])


def downgrade() -> None:
    op.drop_constraint("up_books_name", "books", type_="unique")
