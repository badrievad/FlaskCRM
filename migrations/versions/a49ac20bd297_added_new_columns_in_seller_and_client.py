"""added new columns in Seller and Client

Revision ID: a49ac20bd297
Revises: 79f21326c92a
Create Date: 2024-09-17 09:55:20.877115

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a49ac20bd297"
down_revision = "79f21326c92a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "banks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("inn", sa.String(length=20), nullable=False),
        sa.Column("kpp", sa.String(length=20), nullable=False),
        sa.Column("bic", sa.String(length=20), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("correspondent_account", sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("clients", schema=None) as batch_op:
        batch_op.add_column(sa.Column("okato", sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column("based_on", sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column("bank_id", sa.Integer(), nullable=True))
        batch_op.create_unique_constraint(None, ["inn"])
        batch_op.create_foreign_key(None, "banks", ["bank_id"], ["id"])

    with op.batch_alter_table("sellers", schema=None) as batch_op:
        batch_op.add_column(sa.Column("okato", sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column("kpp", sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column("based_on", sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column("bank_id", sa.Integer(), nullable=True))
        batch_op.alter_column(
            "inn",
            existing_type=sa.VARCHAR(length=255),
            type_=sa.String(length=20),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "ogrn",
            existing_type=sa.VARCHAR(length=255),
            type_=sa.String(length=20),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "phone",
            existing_type=sa.VARCHAR(length=255),
            type_=sa.String(length=20),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "email",
            existing_type=sa.VARCHAR(length=255),
            type_=sa.String(length=100),
            existing_nullable=True,
        )
        batch_op.drop_constraint("sellers_ogrn_key", type_="unique")
        batch_op.create_foreign_key(None, "banks", ["bank_id"], ["id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("sellers", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.create_unique_constraint("sellers_ogrn_key", ["ogrn"])
        batch_op.alter_column(
            "email",
            existing_type=sa.String(length=100),
            type_=sa.VARCHAR(length=255),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "phone",
            existing_type=sa.String(length=20),
            type_=sa.VARCHAR(length=255),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "ogrn",
            existing_type=sa.String(length=20),
            type_=sa.VARCHAR(length=255),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "inn",
            existing_type=sa.String(length=20),
            type_=sa.VARCHAR(length=255),
            existing_nullable=False,
        )
        batch_op.drop_column("bank_id")
        batch_op.drop_column("based_on")
        batch_op.drop_column("kpp")
        batch_op.drop_column("okato")

    with op.batch_alter_table("clients", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_constraint(None, type_="unique")
        batch_op.drop_column("bank_id")
        batch_op.drop_column("based_on")
        batch_op.drop_column("okato")

    op.drop_table("banks")
    # ### end Alembic commands ###