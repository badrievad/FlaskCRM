"""added new column item_type

Revision ID: b51427ef14a1
Revises: 4d4c1369bc86
Create Date: 2024-07-16 17:27:12.934237

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b51427ef14a1"
down_revision = "4d4c1369bc86"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("leas_calculator", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("item_type", sa.String(length=150), nullable=True)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("leas_calculator", schema=None) as batch_op:
        batch_op.drop_column("item_type")

    # ### end Alembic commands ###