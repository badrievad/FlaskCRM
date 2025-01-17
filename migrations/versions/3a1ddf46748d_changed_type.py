"""changed type

Revision ID: 3a1ddf46748d
Revises: 3d9af4432d4d
Create Date: 2024-08-20 17:43:23.922424

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3a1ddf46748d"
down_revision = "3d9af4432d4d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("leas_calculator", schema=None) as batch_op:
        batch_op.alter_column(
            "item_price",
            existing_type=sa.NUMERIC(precision=10, scale=2),
            type_=sa.Float(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "foreign_price",
            existing_type=sa.NUMERIC(precision=10, scale=2),
            type_=sa.Float(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "initial_payment",
            existing_type=sa.NUMERIC(precision=10, scale=2),
            type_=sa.Float(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "credit_sum",
            existing_type=sa.NUMERIC(precision=10, scale=2),
            type_=sa.Float(),
            existing_nullable=True,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("leas_calculator", schema=None) as batch_op:
        batch_op.alter_column(
            "credit_sum",
            existing_type=sa.Float(),
            type_=sa.NUMERIC(precision=10, scale=2),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "initial_payment",
            existing_type=sa.Float(),
            type_=sa.NUMERIC(precision=10, scale=2),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "foreign_price",
            existing_type=sa.Float(),
            type_=sa.NUMERIC(precision=10, scale=2),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "item_price",
            existing_type=sa.Float(),
            type_=sa.NUMERIC(precision=10, scale=2),
            existing_nullable=True,
        )

    # ### end Alembic commands ###
