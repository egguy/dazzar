"""3/ Add index to vip_mmr

Revision ID: 5204ca453334
Revises: d2788e6855d8
Create Date: 2016-11-25 10:02:29.908146

"""

# revision identifiers, used by Alembic.
revision = '5204ca453334'
down_revision = 'd2788e6855d8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_user_vip_mmr'), 'user', ['vip_mmr'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_vip_mmr'), table_name='user')
    ### end Alembic commands ###