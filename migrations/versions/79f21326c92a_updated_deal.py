"""updated Deal

Revision ID: 79f21326c92a
Revises: 002c17453b62
Create Date: 2024-09-16 09:46:50.168481

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "79f21326c92a"
down_revision = "002c17453b62"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("deals", schema=None) as batch_op:
        batch_op.add_column(sa.Column("sequence_number", sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column("year", sa.String(length=2), nullable=False))
        batch_op.create_unique_constraint(
            "uq_sequence_year", ["sequence_number", "year"]
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("deals", schema=None) as batch_op:
        batch_op.drop_constraint("uq_sequence_year", type_="unique")
        batch_op.drop_column("year")
        batch_op.drop_column("sequence_number")

    # ### end Alembic commands ###