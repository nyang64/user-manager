"""update_facility_ext_id_length

Revision ID: 9ca1d19fc484
Revises: 2f151c96b0a9
Create Date: 2021-08-17 14:33:41.705359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ca1d19fc484'
down_revision = '2f151c96b0a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('facilities', 'external_facility_id',
               existing_type=sa.VARCHAR(length=6),
               type_=sa.String(length=10),
               existing_nullable=False,
               schema='ES')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('facilities', 'external_facility_id',
               existing_type=sa.String(length=10),
               type_=sa.VARCHAR(length=6),
               existing_nullable=False,
               schema='ES')
    # ### end Alembic commands ###