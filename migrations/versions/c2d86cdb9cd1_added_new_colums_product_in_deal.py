"""added new colums Product (in Deal)

Revision ID: c2d86cdb9cd1
Revises: cb8a2738709c
Create Date: 2024-06-08 18:43:48.603863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2d86cdb9cd1'
down_revision = 'cb8a2738709c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('deals', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product', sa.String(length=50), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('deals', schema=None) as batch_op:
        batch_op.drop_column('product')

    # ### end Alembic commands ###