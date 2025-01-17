"""added new columns increase_rate

Revision ID: 5b16225042f1
Revises: 3c231ce74928
Create Date: 2024-11-02 10:21:08.562202

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5b16225042f1"
down_revision = "3c231ce74928"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("main_annuity", schema=None) as batch_op:
        batch_op.add_column(sa.Column("increase_rate", sa.Float(), nullable=False))

    with op.batch_alter_table("main_differentiated", schema=None) as batch_op:
        batch_op.add_column(sa.Column("increase_rate", sa.Float(), nullable=False))

    with op.batch_alter_table("main_regression", schema=None) as batch_op:
        batch_op.add_column(sa.Column("increase_rate", sa.Float(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("main_regression", schema=None) as batch_op:
        batch_op.drop_column("increase_rate")

    with op.batch_alter_table("main_differentiated", schema=None) as batch_op:
        batch_op.drop_column("increase_rate")

    with op.batch_alter_table("main_annuity", schema=None) as batch_op:
        batch_op.drop_column("increase_rate")

    # ### end Alembic commands ###
