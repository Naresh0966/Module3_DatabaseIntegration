"""add course_schedules table

Revision ID: 003
Revises: 002
Create Date: 2024-01-03 10:00:00

Task 2 — Step 102:
Creates the new course_schedules table.
upgrade()   → creates the table
downgrade() → drops the table
"""

from alembic import op
import sqlalchemy as sa

# ─── Revision identifiers ─────────────────────────────────────────────────────
revision      = '003'
down_revision = '002'        # points back to migration 002
branch_labels = None
depends_on    = None


# ─── upgrade() ───────────────────────────────────────────────────────────────
# Applied when you run:  alembic upgrade head  (or  alembic upgrade 003)
def upgrade() -> None:
    op.create_table(
        'course_schedules',
        sa.Column('schedule_id', sa.Integer(),    primary_key=True, autoincrement=True),
        sa.Column('course_id',   sa.Integer(),    nullable=False),
        sa.Column('day_of_week', sa.String(10),   nullable=False),  # e.g. 'Monday'
        sa.Column('start_time',  sa.Time(),        nullable=False),
        sa.Column('end_time',    sa.Time(),        nullable=False),
        sa.ForeignKeyConstraint(['course_id'], ['courses.course_id']),
    )
    # ── What to observe after running upgrade ─────────────────────────────────
    # In MySQL Workbench: SHOW TABLES; → course_schedules appears
    # DESCRIBE course_schedules; → shows all 5 columns
    # ─────────────────────────────────────────────────────────────────────────


# ─── downgrade() ─────────────────────────────────────────────────────────────
# Applied when you run:  alembic downgrade -1  (or  alembic downgrade 002)
def downgrade() -> None:
    op.drop_table('course_schedules')
    # ── What to observe after running downgrade ───────────────────────────────
    # SHOW TABLES; → course_schedules is gone
    # alembic current → shows revision 002
    # ─────────────────────────────────────────────────────────────────────────
