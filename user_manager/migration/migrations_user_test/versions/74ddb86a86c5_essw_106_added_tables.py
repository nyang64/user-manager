"""ESSW-106 Added  tables

Revision ID: 74ddb86a86c5
Revises: 64f2ec8028c3
Create Date: 2021-03-09 20:09:07.873130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74ddb86a86c5'
down_revision = '64f2ec8028c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('provider_role_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='ES'
    )
    op.create_table('providers_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('provider_role_id', sa.Integer(), nullable=True),
    sa.Column('provider_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['provider_id'], ['ES.providers.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['provider_role_id'], ['ES.provider_role_types.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='ES'
    )
    op.create_table('patients_providers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('provider_role_id', sa.Integer(), nullable=True),
    sa.Column('provider_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['ES.patients.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['provider_id'], ['ES.providers.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['provider_role_id'], ['ES.provider_role_types.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='ES'
    )
    op.create_table('patches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('patient_device_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['patient_device_id'], ['ES.patients_devices.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='ES'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('patches', schema='ES')
    op.drop_table('patients_providers', schema='ES')
    op.drop_table('providers_roles', schema='ES')
    op.drop_table('provider_role_types', schema='ES')
    # ### end Alembic commands ###
