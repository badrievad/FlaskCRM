"""added new tables

Revision ID: 640842fe23c0
Revises: b11749941bb0
Create Date: 2024-06-03 14:35:18.877296

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "640842fe23c0"
down_revision = "b11749941bb0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "deal_steps",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("step1_approved", sa.Boolean(), nullable=True),
        sa.Column("step1_time", sa.String(length=50), nullable=True),
        sa.Column("step1_user", sa.String(length=50), nullable=True),
        sa.Column("step2_approved", sa.Boolean(), nullable=True),
        sa.Column("step2_time", sa.String(length=50), nullable=True),
        sa.Column("step2_user", sa.String(length=50), nullable=True),
        sa.Column("step3_approved", sa.Boolean(), nullable=True),
        sa.Column("step3_time", sa.String(length=50), nullable=True),
        sa.Column("step3_user", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "deals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("deals")
    op.drop_table("deal_steps")
    # ### end Alembic commands ###
