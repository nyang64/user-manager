"""Modifications to Salvos table

Revision ID: 89943f1d2444
Revises: b32d00965447
Create Date: 2021-04-19 09:40:22.974984

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "89943f1d2444"
down_revision = "b32d00965447"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "salvos", sa.Column("shock_count", sa.Integer(), nullable=True), schema="ES"
    )
    op.add_column(
        "salvos", sa.Column("shock_duration", sa.Numeric(), nullable=True), schema="ES"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("salvos", "shock_duration", schema="ES")
    op.drop_column("salvos", "shock_count", schema="ES")
    # ### end Alembic commands ###
