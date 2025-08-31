from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6bb3dab713e3' # This should match the filename
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table('courses') as batch_op:
        batch_op.alter_column('id',
                              existing_type=sa.Integer(),
                              type_=sa.String(36),
                              existing_nullable=True)


def downgrade():
    with op.batch_alter_table('courses') as batch_op:
        batch_op.alter_column('id',
                              existing_type=sa.String(36),
                              type_=sa.Integer(),
                              existing_nullable=True)