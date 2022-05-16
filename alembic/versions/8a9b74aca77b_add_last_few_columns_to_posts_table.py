"""add last few columns to posts table

Revision ID: 8a9b74aca77b
Revises: afe3a23a5619
Create Date: 2022-05-10 16:07:41.261289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8a9b74aca77b"
down_revision = "afe3a23a5619"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
