"""added new column deal_path

Revision ID: c46b2592e0db
Revises: d0ff44e14d70
Create Date: 2024-08-12 13:54:15.218519

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c46b2592e0db"
down_revision = "d0ff44e14d70"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("deals", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("deal_path", sa.String(length=500), nullable=True)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("deals", schema=None) as batch_op:
        batch_op.drop_column("deal_path")

    # ### end Alembic commands ###
