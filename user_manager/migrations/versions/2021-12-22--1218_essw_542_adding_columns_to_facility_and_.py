"""ESSW-542:Adding columns to facility and providers

Revision ID: e392a81364a3
Revises: 89c3a0299380
Create Date: 2021-12-22 12:18:34.791860

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import expression


# revision identifiers, used by Alembic.
revision = 'e392a81364a3'
down_revision = '89c3a0299380'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('facilities', sa.Column('primary_contact_id', sa.Integer(), nullable=True), schema='ES')
    op.create_foreign_key(None, 'facilities', 'users', ['primary_contact_id'], ['id'], source_schema='ES', referent_schema='ES', ondelete='CASCADE')
    op.add_column('providers', sa.Column('is_primary', sa.Boolean(), nullable=False, server_default=expression.false()), schema='ES')
    op.drop_column('study_managers', 'facility_id', schema='ES')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('study_managers', sa.Column('facility_id', sa.VARCHAR(length=50), autoincrement=False, nullable=True), schema='ES')
    op.drop_column('providers', 'is_primary', schema='ES')
    op.drop_column('facilities', 'primary_contact_id', schema='ES')
    # ### end Alembic commands ###
