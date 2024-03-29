"""add_providers_roles_table

Revision ID: 7d03fc575517
Revises: e6ba6f9e06fc
Create Date: 2021-03-16 15:35:40.329308

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d03fc575517'
down_revision = 'e6ba6f9e06fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('providers_roles', schema='ES')
    # ### end Alembic commands ###
