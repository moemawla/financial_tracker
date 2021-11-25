"""Added creator_id to transactions

Revision ID: 39389c70a205
Revises: afa86ff1b35d
Create Date: 2021-11-25 10:33:40.912313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39389c70a205'
down_revision = 'afa86ff1b35d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('creator_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'transactions', 'flasklogin-users', ['creator_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.drop_column('transactions', 'creator_id')
    # ### end Alembic commands ###
