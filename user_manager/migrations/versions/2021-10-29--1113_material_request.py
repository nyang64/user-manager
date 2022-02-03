"""material request

Revision ID: e7bf1b93589f
Revises: 4ff78f46eaa1
Create Date: 2021-10-29 11:13:00.028181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7bf1b93589f'
down_revision = '4ff78f46eaa1'
branch_labels = None
depends_on = None

MATERIAL_REQ_SEQUENCE = sa.Sequence('material_req_seq', start=100000, increment=1, schema="ES")

def upgrade():
    op.execute(sa.schema.CreateSequence(MATERIAL_REQ_SEQUENCE))

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('material_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('request_number', sa.Integer(), server_default=sa.text('nextval(\'"ES".material_req_seq\')'), nullable=True),
    sa.Column('num_items', sa.Integer(), nullable=False),
    sa.Column('request_date', sa.DateTime(), nullable=True),
    sa.Column('requested_user', sa.Integer(), nullable=False),
    sa.Column('request_log_location', sa.String(length=200), nullable=True),
    sa.ForeignKeyConstraint(['requested_user'], ['ES.users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='ES'
    )
    # ### end Alembic commands ###


def downgrade():
    op.execute(sa.schema.DropSequence(MATERIAL_REQ_SEQUENCE))
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('material_requests', schema='ES')
    # ### end Alembic commands ###