"""added new table (users)

Revision ID: 887495d7e797
Revises: 
Create Date: 2024-06-03 14:06:19.893058

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "887495d7e797"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("login", sa.String(length=50), nullable=True),
        sa.Column("password", sa.String(length=50), nullable=True),
        sa.Column("blocked", sa.Boolean(), nullable=True),
        sa.Column("role", sa.String(length=50), nullable=True),
        sa.Column("fullname", sa.String(), nullable=True),
        sa.Column("email", sa.String(length=50), nullable=True),
        sa.Column("url_photo", sa.String(), nullable=True),
        sa.Column("worknumber", sa.String(), nullable=True),
        sa.Column("mobilenumber", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("login"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
