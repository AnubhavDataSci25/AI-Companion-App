"""fix embedding dimension to 3072

Revision ID: d48e70b45811
Revises: d95b677dec80
Create Date: 2026-07-29 02:11:56.207875

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'd48e70b45811'
down_revision = 'd95b677dec80'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("UPDATE memories SET embedding = NULL WHERE embedding IS NOT NULL")
    op.execute("ALTER TABLE memories ALTER COLUMN embedding TYPE vector(3072)")


def downgrade():
    op.execute("UPDATE memories SET embedding = NULL WHERE embedding IS NOT NULL")
    op.execute("ALTER TABLE memories ALTER COLUMN embedding TYPE vector(768)")
