"""deleted mayak_str and tracker_str

Revision ID: e16caa503744
Revises: 7529e00325a5
Create Date: 2024-12-09 11:01:16.718564

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e16caa503744"
down_revision = "7529e00325a5"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("leas_calculator", schema=None) as batch_op:
        batch_op.alter_column(
            "tracker",
            existing_type=sa.DOUBLE_PRECISION(precision=53),
            type_=sa.Integer(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "mayak",
            existing_type=sa.DOUBLE_PRECISION(precision=53),
            type_=sa.Integer(),
            existing_nullable=True,
        )
        batch_op.drop_column("tracker_str")
        batch_op.drop_column("mayak_str")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("leas_calculator", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "mayak_str", sa.VARCHAR(length=50), autoincrement=False, nullable=True
            )
        )
        batch_op.add_column(
            sa.Column(
                "tracker_str", sa.VARCHAR(length=50), autoincrement=False, nullable=True
            )
        )
        batch_op.alter_column(
            "mayak",
            existing_type=sa.Integer(),
            type_=sa.DOUBLE_PRECISION(precision=53),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "tracker",
            existing_type=sa.Integer(),
            type_=sa.DOUBLE_PRECISION(precision=53),
            existing_nullable=True,
        )

    # ### end Alembic commands ###
