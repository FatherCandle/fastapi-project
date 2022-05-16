"""Create post table

Revision ID: bfd5434cee77
Revises: 
Create Date: 2022-05-10 15:29:47.224725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bfd5434cee77"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )


def downgrade():
    op.drop_table("posts")
