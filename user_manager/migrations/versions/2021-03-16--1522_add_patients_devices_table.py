"""add_patients_devices_table

Revision ID: e136da258567
Revises: 903c7bdef169
Create Date: 2021-03-16 15:22:21.804030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e136da258567'
down_revision = '903c7bdef169'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('patients_devices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('device_serial_number', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['ES.patients.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='ES'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('patients_devices', schema='ES')
    # ### end Alembic commands ###