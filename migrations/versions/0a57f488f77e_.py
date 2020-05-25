"""empty message

Revision ID: 0a57f488f77e
Revises: 814a39f77cca
Create Date: 2020-04-17 12:25:09.676220

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '0a57f488f77e'
down_revision = '8b66f1dd020c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('moving_average_specs',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('candle_in_human_readable', sa.String(length=4), nullable=False),
    sa.Column('candle_in_seconds', sa.INTEGER(), nullable=False),
    sa.Column('order', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id', name='moving_average_specs_pkey')
    )
    op.create_table('moving_averages',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('value', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('time_range', postgresql.INT4RANGE, nullable=False),
    sa.Column('first_close_time', sa.INTEGER(), nullable=False),
    sa.Column('spec_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['spec_id'], ['moving_average_specs.id'], ),
    sa.PrimaryKeyConstraint('id', name='moving_averages_pkey')
    )


def downgrade():
    op.drop_table('moving_averages')
    op.drop_table('moving_average_specs')
