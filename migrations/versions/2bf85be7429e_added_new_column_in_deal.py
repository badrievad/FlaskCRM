"""added new column in Deal

Revision ID: 2bf85be7429e
Revises: 7d4f65320b03
Create Date: 2024-08-07 16:36:31.217259

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2bf85be7429e"
down_revision = "7d4f65320b03"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("deals", schema=None) as batch_op:
        batch_op.add_column(sa.Column("deals_count", sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("deals", schema=None) as batch_op:
        batch_op.drop_column("deals_count")

    # ### end Alembic commands ###
