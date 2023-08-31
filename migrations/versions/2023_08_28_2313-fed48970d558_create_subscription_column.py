"""Create subscription column

Revision ID: fed48970d558
Revises: cc93cd4bccda
Create Date: 2023-08-28 23:13:08.504571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fed48970d558'
down_revision: Union[str, None] = 'cc93cd4bccda'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscription',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('subscriber', sa.Integer(), nullable=False),
    sa.Column('account', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['account'], ['user.id'], ),
    sa.ForeignKeyConstraint(['subscriber'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscription_account'), 'subscription', ['account'], unique=False)
    op.create_index(op.f('ix_subscription_id'), 'subscription', ['id'], unique=True)
    op.create_index(op.f('ix_subscription_subscriber'), 'subscription', ['subscriber'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_subscription_subscriber'), table_name='subscription')
    op.drop_index(op.f('ix_subscription_id'), table_name='subscription')
    op.drop_index(op.f('ix_subscription_account'), table_name='subscription')
    op.drop_table('subscription')
    # ### end Alembic commands ###