"""add foreign key to post table

Revision ID: afe3a23a5619
Revises: 3d846ac996bb
Create Date: 2022-05-10 16:04:06.103498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "afe3a23a5619"
down_revision = "3d846ac996bb"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade():
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
