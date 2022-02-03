"""Modifications for patient add or edit

Revision ID: 3a83bbdac417
Revises: e7bf1b93589f
Create Date: 2021-11-11 14:07:33.895570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a83bbdac417'
down_revision = 'e7bf1b93589f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('patient_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('mobile_model', sa.String(length=20), nullable=False),
    sa.Column('mobile_os_version', sa.String(length=20), nullable=False),
    sa.Column('other_phone', sa.String(length=12), nullable=False),
    sa.Column('pa_setting_back', sa.String(length=12), nullable=True),
    sa.Column('pa_setting_front', sa.String(length=12), nullable=True),
    sa.Column('shoulder_strap_back', sa.String(length=12), nullable=True),
    sa.Column('shoulder_strap_front', sa.String(length=12), nullable=True),
    sa.Column('starter_kit_lot_number', sa.String(length=20), nullable=True),
    sa.Column('upper_patch_setting', sa.String(length=20), nullable=False),
    sa.Column('enrollment_notes', sa.String(length=300), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['ES.patients.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='ES'
    )
    op.add_column('patients', sa.Column('emergency_contact_relationship', sa.String(length=30), nullable=True), schema='ES')
    op.add_column('patients_patches', sa.Column('is_applied', sa.Boolean(), nullable=True), schema='ES')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('patients_patches', 'is_applied', schema='ES')
    op.drop_column('patients', 'emergency_contact_relationship', schema='ES')
    op.drop_table('patient_details', schema='ES')
    # ### end Alembic commands ###