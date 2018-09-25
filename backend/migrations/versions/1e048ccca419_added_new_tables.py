"""Added new tables

Revision ID: 1e048ccca419
Revises: 
Create Date: 2018-09-19 00:41:14.680805

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e048ccca419'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('updated_date', sa.DateTime(), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('created_date', sa.DateTime(), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user_credential',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('updated_date', sa.DateTime(), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('created_date', sa.DateTime(), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_credential_username'), 'user_credential', ['username'], unique=True)
    op.create_table('task',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('updated_date', sa.DateTime(), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('created_date', sa.DateTime(), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_credential.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('todo',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('created_date', sa.DateTime(), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('task_id')
    )
    op.create_table('todo_tag',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('todo_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['todo_id'], ['todo.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('todo_id', 'tag_id', name='unique_todo_tag_combination')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todo_tag')
    op.drop_table('todo')
    op.drop_table('task')
    op.drop_index(op.f('ix_user_credential_username'), table_name='user_credential')
    op.drop_table('user_credential')
    op.drop_table('tag')
    # ### end Alembic commands ###
