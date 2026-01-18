"""create video table

Revision ID: 02df633d5649
Revises: None
Create Date: 2026-01-18 04:41:15.017714
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02df633d5649'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'video',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE')
    )


def downgrade():
    op.drop_table('video')