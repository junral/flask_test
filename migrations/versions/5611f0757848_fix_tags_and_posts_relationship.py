"""fix tags and posts relationship

Revision ID: 5611f0757848
Revises: f595298a239f
Create Date: 2017-12-04 10:45:17.610787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5611f0757848'
down_revision = 'f595298a239f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], )
    )
    op.drop_table('post_tag_relationship')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_tag_relationship',
    sa.Column('post_id', sa.INTEGER(), nullable=True),
    sa.Column('tag_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], )
    )
    op.drop_table('tags')
    # ### end Alembic commands ###