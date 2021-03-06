"""Init

Revision ID: cea401a7b5e4
Revises: 
Create Date: 2022-07-20 09:35:46.981025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cea401a7b5e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('note', sa.String(length=100), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('description', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('phone', sa.String(length=50), nullable=False),
    sa.Column('address', sa.String(length=150), nullable=False),
    sa.Column('birthday', sa.String(length=150), nullable=False),
    sa.Column('done', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('records')
    op.drop_table('notes')
    # ### end Alembic commands ###
