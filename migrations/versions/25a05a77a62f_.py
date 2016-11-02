"""empty message

Revision ID: 25a05a77a62f
Revises: None
Create Date: 2016-11-02 22:22:01.140570

"""

# revision identifiers, used by Alembic.
revision = '25a05a77a62f'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('match',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('password', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_match_created'), 'match', ['created'], unique=False)
    op.create_index(op.f('ix_match_status'), 'match', ['status'], unique=False)
    user_permissions = op.create_table('user_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('nickname', sa.String(length=20), nullable=True),
    sa.Column('current_match', sa.Integer(), nullable=True),
    sa.Column('last_scan', sa.DateTime(), nullable=True),
    sa.Column('solo_mmr', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['current_match'], ['match.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_nickname'), 'user', ['nickname'], unique=False)
    op.create_table('permissions',
    sa.Column('permission_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['permission_id'], ['user_permission.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('queued_player',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('queue_name', sa.String(length=20), nullable=False),
    sa.Column('added', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_queued_player_added'), 'queued_player', ['added'], unique=False)
    ### end Alembic commands ###

    ### Add permissions
    op.bulk_insert(user_permissions,
                   [
                       {'name': 'admin'},
                       {'name': 'play_vip'},
                       {'name': 'vouch_vip'}
                   ])
    ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_queued_player_added'), table_name='queued_player')
    op.drop_table('queued_player')
    op.drop_table('permissions')
    op.drop_index(op.f('ix_user_nickname'), table_name='user')
    op.drop_table('user')
    op.drop_table('user_permission')
    op.drop_index(op.f('ix_match_status'), table_name='match')
    op.drop_index(op.f('ix_match_created'), table_name='match')
    op.drop_table('match')
    ### end Alembic commands ###