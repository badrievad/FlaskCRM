"""added new columns travel expr

Revision ID: f5ab57294bb6
Revises: f9d46fff6b2a
Create Date: 2024-08-19 15:47:33.557021

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f5ab57294bb6"
down_revision = "f9d46fff6b2a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("leas_calculator", schema=None) as batch_op:
        batch_op.add_column(sa.Column("depr_transport", sa.Float(), nullable=True))
        batch_op.add_column(
            sa.Column("depr_transport_str", sa.String(length=50), nullable=True)
        )
        batch_op.add_column(sa.Column("travel", sa.Float(), nullable=True))
        batch_op.add_column(
            sa.Column("travel_str", sa.String(length=50), nullable=True)
        )
        batch_op.add_column(sa.Column("stationery", sa.Float(), nullable=True))
        batch_op.add_column(
            sa.Column("stationery_str", sa.String(length=50), nullable=True)
        )
        batch_op.add_column(sa.Column("internet", sa.Float(), nullable=True))
        batch_op.add_column(
            sa.Column("internet_str", sa.String(length=50), nullable=True)
        )
        batch_op.add_column(sa.Column("pledge", sa.Float(), nullable=True))
        batch_op.add_column(
            sa.Column("pledge_str", sa.String(length=50), nullable=True)
        )
        batch_op.add_column(sa.Column("bank_pledge", sa.Float(), nullable=True))
        batch_op.add_column(
            sa.Column("bank_pledge_str", sa.String(length=50), nullable=True)
        )
        batch_op.add_column(sa.Column("express", sa.Float(), nullable=True))
        batch_op.add_column(
            sa.Column("express_str", sa.String(length=50), nullable=True)
        )
        batch_op.add_column(sa.Column("egrn", sa.Float(), nullable=True))
        batch_op.add_column(sa.Column("egrn_str", sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column("egrul", sa.Float(), nullable=True))
        batch_op.add_column(sa.Column("egrul_str", sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("leas_calculator", schema=None) as batch_op:
        batch_op.drop_column("egrul_str")
        batch_op.drop_column("egrul")
        batch_op.drop_column("egrn_str")
        batch_op.drop_column("egrn")
        batch_op.drop_column("express_str")
        batch_op.drop_column("express")
        batch_op.drop_column("bank_pledge_str")
        batch_op.drop_column("bank_pledge")
        batch_op.drop_column("pledge_str")
        batch_op.drop_column("pledge")
        batch_op.drop_column("internet_str")
        batch_op.drop_column("internet")
        batch_op.drop_column("stationery_str")
        batch_op.drop_column("stationery")
        batch_op.drop_column("travel_str")
        batch_op.drop_column("travel")
        batch_op.drop_column("depr_transport_str")
        batch_op.drop_column("depr_transport")

    # ### end Alembic commands ###