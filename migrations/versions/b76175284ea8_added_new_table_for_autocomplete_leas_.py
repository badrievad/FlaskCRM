"""added new table for autocomplete leas_items

Revision ID: b76175284ea8
Revises: efb454aa8cba
Create Date: 2024-07-17 16:20:32.223787

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b76175284ea8"
down_revision = "efb454aa8cba"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "leas_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=500), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("leas_items")
    # ### end Alembic commands ###