"""empty message

Revision ID: 38bd83c30f6c
Revises: 89428e56944f
Create Date: 2017-04-10 13:10:02.917753

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38bd83c30f6c'
down_revision = '89428e56944f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('domain', sa.Column('contact_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'domain', 'contact', ['contact_id'], ['id'])
    op.add_column('host', sa.Column('domain_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'host', 'domain', ['domain_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'host', type_='foreignkey')
    op.drop_column('host', 'domain_id')
    op.drop_constraint(None, 'domain', type_='foreignkey')
    op.drop_column('domain', 'contact_id')
    # ### end Alembic commands ###
