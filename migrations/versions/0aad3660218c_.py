"""empty message

Revision ID: 0aad3660218c
Revises: 0a57f488f77e
Create Date: 2020-05-27 21:50:14.313129

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0aad3660218c'
down_revision = '0a57f488f77e'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('moving_averages', 'spec_id', nullable=False, new_column_name='ma_spec_id')
    op.create_table('deviation_specs',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('percentage', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('ma_spec_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['ma_spec_id'], ['moving_average_specs.id'], ),
    sa.PrimaryKeyConstraint('id', name='deviation_specs_pkey')
    )
    op.create_table('deviations',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('time', sa.DateTime(timezone=True), nullable=False),
    sa.Column('deviation_spec_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['deviation_spec_id'], ['deviation_specs.id'], ),
    sa.PrimaryKeyConstraint('id', name='deviations_pkey')
    )


def downgrade():
    op.alter_column('moving_averages', 'ma_spec_id', nullable=False, new_column_name='spec_id')
    op.drop_table('deviations')
    op.drop_table('deviation_specs')
