"""add_patient_facilities_table

Revision ID: d358f61fd4b3
Revises: 517faa81285d
Create Date: 2022-05-19 17:19:19.482621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd358f61fd4b3'
down_revision = '517faa81285d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('patient_facilities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('facility_id', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['facility_id'], ['ES.facilities.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['patient_id'], ['ES.patients.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='ES'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('patient_facilities', schema='ES')
    # ### end Alembic commands ###