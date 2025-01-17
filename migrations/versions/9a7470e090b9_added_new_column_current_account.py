"""added new column current_account

Revision ID: 9a7470e090b9
Revises: a49ac20bd297
Create Date: 2024-09-17 10:26:12.246617

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9a7470e090b9"
down_revision = "a49ac20bd297"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("clients", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("current_account", sa.String(length=30), nullable=True)
        )

    with op.batch_alter_table("sellers", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("current_account", sa.String(length=30), nullable=True)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("sellers", schema=None) as batch_op:
        batch_op.drop_column("current_account")

    with op.batch_alter_table("clients", schema=None) as batch_op:
        batch_op.drop_column("current_account")

    # ### end Alembic commands ###
