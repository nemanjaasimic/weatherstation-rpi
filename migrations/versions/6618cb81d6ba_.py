"""empty message

Revision ID: 6618cb81d6ba
Revises: 
Create Date: 2024-08-26 19:31:16.489317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6618cb81d6ba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('measurement',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('time', sa.Time(), nullable=False),
    sa.Column('altitude', sa.Float(precision=2), nullable=False),
    sa.Column('longitude', sa.String(), nullable=False),
    sa.Column('latitude', sa.String(), nullable=False),
    sa.Column('temperature', sa.Float(precision=2), nullable=False),
    sa.Column('relative_humidity', sa.Float(precision=2), nullable=False),
    sa.Column('globe_temperature', sa.Float(precision=2), nullable=False),
    sa.Column('wind_speed', sa.Float(precision=2), nullable=False),
    sa.Column('limited_wind_speed', sa.Float(precision=2), nullable=False),
    sa.Column('pm_2_5', sa.Float(precision=2), nullable=False),
    sa.Column('pm_10', sa.Float(precision=2), nullable=False),
    sa.Column('uv_b', sa.Float(precision=2), nullable=False),
    sa.Column('location_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('measurement')
    op.drop_table('location')
    # ### end Alembic commands ###
