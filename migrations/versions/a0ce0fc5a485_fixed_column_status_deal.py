"""fixed column Status (Deal)

Revision ID: a0ce0fc5a485
Revises: ec04e43a5e0f
Create Date: 2024-06-05 20:46:35.818730

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a0ce0fc5a485"
down_revision = "ec04e43a5e0f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("deals", schema=None) as batch_op:
        batch_op.alter_column(
            "status", existing_type=sa.VARCHAR(length=20), nullable=False
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("deals", schema=None) as batch_op:
        batch_op.alter_column(
            "status", existing_type=sa.VARCHAR(length=20), nullable=True
        )

    # ### end Alembic commands ###
