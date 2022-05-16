"""add content column to posts table

Revision ID: 8240ff8616b0
Revises: bfd5434cee77
Create Date: 2022-05-10 15:36:26.730134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8240ff8616b0"
down_revision = "bfd5434cee77"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade():
    op.drop_column("posts", "content")
