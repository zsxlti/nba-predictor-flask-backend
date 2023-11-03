"""empty message

Revision ID: dcc186a9914b
Revises: 453ddd4c8c6d
Create Date: 2023-10-30 12:17:53.668444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcc186a9914b'
down_revision = '453ddd4c8c6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('players', schema=None) as batch_op:
        batch_op.alter_column('team_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_constraint('players_team_id_fkey', type_='foreignkey')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('players', schema=None) as batch_op:
        batch_op.create_foreign_key('players_team_id_fkey', 'teams', ['team_id'], ['id'])
        batch_op.alter_column('team_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###