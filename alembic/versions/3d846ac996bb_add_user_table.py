"""Add user table

Revision ID: 3d846ac996bb
Revises: 8240ff8616b0
Create Date: 2022-05-10 15:55:47.355823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3d846ac996bb"
down_revision = "8240ff8616b0"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade():
    op.drop_table("users")
