"""empty message

Revision ID: 8b66f1dd020c
Revises: 
Create Date: 2020-05-02 15:53:25.057768

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8b66f1dd020c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('trades',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('price', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('quantity', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('quote_quantity', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('time', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('is_buyer_maker', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('is_best_match', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='trades_pkey')
    )
    op.create_table('prices',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('value', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('time', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='prices_pkey')
    )


def downgrade():
    pass
