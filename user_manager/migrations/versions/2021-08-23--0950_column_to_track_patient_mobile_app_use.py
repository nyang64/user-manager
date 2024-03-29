"""Column to track  patient mobile app use

Revision ID: 9d2b241d85bf
Revises: c08c0c921311
Create Date: 2021-08-23 09:50:44.738703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d2b241d85bf'
down_revision = 'c08c0c921311'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('patients', sa.Column('mobile_app_user', sa.Boolean(), nullable=True), schema='ES')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('patients', 'mobile_app_user', schema='ES')
    # ### end Alembic commands ###
