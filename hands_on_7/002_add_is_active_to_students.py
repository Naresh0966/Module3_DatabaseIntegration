"""add is_active to students

Revision ID: 002
Revises: 001
Create Date: 2024-01-02 10:00:00

Task 2 — Steps 98–101:
Adds is_active BOOLEAN column to students table.
upgrade()   → adds the column
downgrade() → drops the column (safe rollback)
"""

from alembic import op
import sqlalchemy as sa

# ─── Revision identifiers ─────────────────────────────────────────────────────
revision      = '002'
down_revision = '001'        # points back to migration 001
branch_labels = None
depends_on    = None


# ─── upgrade() ───────────────────────────────────────────────────────────────
# Applied when you run:  alembic upgrade head  (or  alembic upgrade 002)
def upgrade() -> None:
    op.add_column(
        'students',
        sa.Column(
            'is_active',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('1')   # MySQL: 1=TRUE  |  PostgreSQL: use 'true'
        )
    )
    # ── What to observe after running upgrade ─────────────────────────────────
    # In MySQL Workbench: DESCRIBE students;
    # You will see is_active column with Type=tinyint(1), Default=1
    # ─────────────────────────────────────────────────────────────────────────


# ─── downgrade() ─────────────────────────────────────────────────────────────
# Applied when you run:  alembic downgrade -1  (or  alembic downgrade 001)
def downgrade() -> None:
    op.drop_column('students', 'is_active')
    # ── What to observe after running downgrade ───────────────────────────────
    # DESCRIBE students; → is_active column is gone
    # alembic current   → shows revision 001 instead of 002
    # ─────────────────────────────────────────────────────────────────────────
