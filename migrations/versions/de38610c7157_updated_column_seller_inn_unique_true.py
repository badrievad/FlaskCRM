"""updated column seller_inn(unique=True)

Revision ID: de38610c7157
Revises: 10e362e2f46c
Create Date: 2024-09-05 09:19:34.814495

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "de38610c7157"
down_revision = "10e362e2f46c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("sellers", schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ["inn"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("sellers", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="unique")

    # ### end Alembic commands ###