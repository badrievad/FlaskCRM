"""added new columns

Revision ID: e9a189869fee
Revises: fa1bc802f99d
Create Date: 2024-10-15 12:37:52.061930

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e9a189869fee"
down_revision = "fa1bc802f99d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("leas_calculator", schema=None) as batch_op:
        batch_op.add_column(sa.Column("agreement_term", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("reduce_percent", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("leas_day", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("service_life", sa.Integer(), nullable=True))
        batch_op.add_column(
            sa.Column("amortization", sa.String(length=150), nullable=True)
        )
        batch_op.add_column(sa.Column("nds_size", sa.Integer(), nullable=True))

    with op.batch_alter_table("tranches", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("tranche_1_payment_deferment", sa.Integer(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("tranche_2_payment_deferment", sa.Integer(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("tranche_3_payment_deferment", sa.Integer(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("tranche_4_payment_deferment", sa.Integer(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("tranche_5_payment_deferment", sa.Integer(), nullable=True)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("tranches", schema=None) as batch_op:
        batch_op.drop_column("tranche_5_payment_deferment")
        batch_op.drop_column("tranche_4_payment_deferment")
        batch_op.drop_column("tranche_3_payment_deferment")
        batch_op.drop_column("tranche_2_payment_deferment")
        batch_op.drop_column("tranche_1_payment_deferment")

    with op.batch_alter_table("leas_calculator", schema=None) as batch_op:
        batch_op.drop_column("nds_size")
        batch_op.drop_column("amortization")
        batch_op.drop_column("service_life")
        batch_op.drop_column("leas_day")
        batch_op.drop_column("reduce_percent")
        batch_op.drop_column("agreement_term")

    # ### end Alembic commands ###
