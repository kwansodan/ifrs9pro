"""updating loan table to make loan id field a string

Revision ID: c1bfd7cf8de8
Revises: 600ce23d9979
Create Date: 2025-02-17 00:41:47.605601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1bfd7cf8de8'
down_revision = '600ce23d9979'
branch_labels = None
depends_on = None


def upgrade():
    # Change loan_no column type to String (VARCHAR)
    op.alter_column('loan', 'loan_no',
                    existing_type=sa.Integer,  # Change this to match the current type
                    type_=sa.String(255),  # Change to VARCHAR(255)
                    existing_nullable=False)

def downgrade():
    # Revert back to Integer (or previous type)
    op.alter_column('loan', 'loan_no',
                    existing_type=sa.String(255),
                    type_=sa.Integer,  # Change this to the original type
                    existing_nullable=False)