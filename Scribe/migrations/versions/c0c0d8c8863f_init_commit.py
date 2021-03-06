"""Init Commit

Revision ID: c0c0d8c8863f
Revises: 
Create Date: 2020-03-06 14:34:39.772168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c0c0d8c8863f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "device_models",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("manufacturer", sa.String(length=120), nullable=False),
        sa.Column("model", sa.String(length=120), nullable=False),
        sa.Column("os", sa.String(length=120), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "groups",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("groupname", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("groupname"),
    )
    op.create_table(
        "proxies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("alias", sa.String(length=120), nullable=False),
        sa.Column("ip", sa.String(length=15), nullable=False),
        sa.Column("port", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=128), nullable=False),
        sa.Column("password", sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("alias"),
    )
    op.create_table(
        "repos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("repo_name", sa.String(length=120), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("repo_name"),
    )
    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ip", sa.String(length=15), nullable=False),
        sa.Column("port", sa.Integer(), nullable=False),
        sa.Column("alias", sa.String(length=120), nullable=False),
        sa.Column("model", sa.String(length=120), nullable=False),
        sa.Column("user", sa.String(length=120), nullable=False),
        sa.Column("password", sa.String(length=120), nullable=False),
        sa.Column("enable", sa.String(length=120), nullable=True),
        sa.Column("last_updated", sa.String(length=32), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("repo", sa.String(length=120), nullable=False),
        sa.Column("proxy", sa.String(length=120), nullable=True),
        sa.ForeignKeyConstraint(
            ["model"],
            ["device_models.id"],
        ),
        sa.ForeignKeyConstraint(
            ["proxy"],
            ["proxies.alias"],
        ),
        sa.ForeignKeyConstraint(
            ["repo"],
            ["repos.repo_name"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ip"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("group", sa.String(length=64), nullable=True),
        sa.Column("password_hash", sa.String(length=128), nullable=False),
        sa.ForeignKeyConstraint(
            ["group"],
            ["groups.groupname"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("password_hash"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    op.create_table(
        "device_associations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("device", sa.String(length=120), nullable=True),
        sa.Column("user", sa.String(length=64), nullable=True),
        sa.Column("group", sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(
            ["device"],
            ["devices.alias"],
        ),
        sa.ForeignKeyConstraint(
            ["group"],
            ["groups.groupname"],
        ),
        sa.ForeignKeyConstraint(
            ["user"],
            ["users.username"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("device_associations")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_table("devices")
    op.drop_table("repos")
    op.drop_table("proxies")
    op.drop_table("groups")
    op.drop_table("device_models")
    # ### end Alembic commands ###
