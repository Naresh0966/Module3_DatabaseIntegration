# run_migrations.py
# Hands-On 7 — Complete Step-by-Step Migration Runner
# ─────────────────────────────────────────────────────────────────────────────
# This file shows every command you need to run in your terminal
# along with what output to expect at each step.
#
# HOW TO USE:
#   Read this file top to bottom.
#   Copy each command block into your terminal and run it.
#   Verify the expected output before moving to the next step.
# ─────────────────────────────────────────────────────────────────────────────

"""
PRE-REQUISITES
──────────────
1. MySQL running locally with college_db_orm database created:
     mysql -u root -p
     CREATE DATABASE college_db_orm;
     EXIT;

2. alembic.ini edited with your credentials:
     sqlalchemy.url = mysql+mysqlconnector://root:yourpassword@localhost/college_db_orm

3. Install packages:
     pip install sqlalchemy alembic mysql-connector-python

4. All files in the same folder:
     hands_on_7/
     ├── alembic.ini
     ├── models.py
     ├── run_migrations.py
     └── migrations/
         ├── env.py
         ├── README
         ├── script.py.mako
         └── versions/
             ├── 001_initial_schema.py
             ├── 002_add_is_active_to_students.py
             └── 003_add_course_schedules_table.py

Open your terminal inside the hands_on_7/ folder for all commands below.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# TASK 1 — Set Up Alembic and Apply Baseline Migration
# ═══════════════════════════════════════════════════════════════════════════════

"""
STEP 92 — Alembic is already initialised.
The `alembic init migrations` command was already run.
You can see the migrations/ folder was created.

STEP 93 — alembic.ini is already configured.
Open alembic.ini and verify this line has your credentials:
  sqlalchemy.url = mysql+mysqlconnector://root:yourpassword@localhost/college_db_orm

STEP 94 — env.py is already configured.
Open migrations/env.py and verify:
  from models import Base
  target_metadata = Base.metadata

STEP 95 — View the generated migration file:
  Open migrations/versions/001_initial_schema.py
  Confirm it has upgrade() and downgrade() functions. ✓

STEP 96 — Apply the first migration:

  COMMAND:
    alembic upgrade 001

  EXPECTED OUTPUT:
    INFO  [alembic.runtime.migration] Context impl MySQLImpl.
    INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
    INFO  [alembic.runtime.migration] Running upgrade  -> 001, initial schema

  VERIFY in MySQL Workbench:
    SHOW TABLES;
    → departments, students, courses, enrollments, professors appear.

    SELECT * FROM alembic_version;
    → Returns one row: 001

STEP 97 — Check current migration status:

  COMMAND:
    alembic current

  EXPECTED OUTPUT:
    INFO  [alembic.runtime.migration] Context impl MySQLImpl.
    001 (head)

  'head' means this is the latest applied migration. ✓
"""

# ═══════════════════════════════════════════════════════════════════════════════
# TASK 2 — Incremental Migrations
# ═══════════════════════════════════════════════════════════════════════════════

"""
STEP 98 — is_active column is already added in models.py.
Open models.py → Student class, you'll see:
  is_active = Column(Boolean, default=True)

STEP 99 — View migration 002:
  Open migrations/versions/002_add_is_active_to_students.py
  Confirm upgrade() adds is_active and downgrade() drops it. ✓

STEP 100 — Apply migration 002:

  COMMAND:
    alembic upgrade 002

  EXPECTED OUTPUT:
    INFO  [alembic.runtime.migration] Running upgrade 001 -> 002, add is_active to students

  VERIFY in MySQL Workbench:
    DESCRIBE students;
    → is_active column appears with Type=tinyint(1), Default=1

STEP 101 — Verify the column:

  In MySQL Workbench run:
    SELECT column_name, data_type, column_default
    FROM information_schema.columns
    WHERE table_name = 'students' AND column_name = 'is_active';

  EXPECTED:
    column_name | data_type | column_default
    is_active   | tinyint   | 1

STEP 102 — Apply migration 003 (CourseSchedule table):

  COMMAND:
    alembic upgrade 003

  EXPECTED OUTPUT:
    INFO  [alembic.runtime.migration] Running upgrade 002 -> 003, add course_schedules table

  VERIFY in MySQL Workbench:
    SHOW TABLES;
    → course_schedules appears

    DESCRIBE course_schedules;
    → schedule_id, course_id, day_of_week, start_time, end_time

STEP 103 — View full migration history:

  COMMAND:
    alembic history --verbose

  EXPECTED OUTPUT:
    Rev: 003 (head)
    Parent: 002
    Path: migrations/versions/003_add_course_schedules_table.py
    add course_schedules table

    Rev: 002
    Parent: 001
    Path: migrations/versions/002_add_is_active_to_students.py
    add is_active to students

    Rev: 001 (base)
    Parent: <base>
    Path: migrations/versions/001_initial_schema.py
    initial schema

  This shows all 3 revisions in the chain. ✓
"""

# ═══════════════════════════════════════════════════════════════════════════════
# TASK 3 — Rollback and Recovery
# ═══════════════════════════════════════════════════════════════════════════════

"""
STEP 104 — Note the current head revision:

  COMMAND:
    alembic current

  EXPECTED OUTPUT:
    003 (head)

  Save this hash — you'll use it to verify you've returned to it after re-apply.

──────────────────────────────────────────────────────────────────────────────
STEP 105 — Rollback ONE step (003 → 002):

  COMMAND:
    alembic downgrade -1

  EXPECTED OUTPUT:
    INFO  [alembic.runtime.migration] Running downgrade 003 -> 002, add course_schedules table

  VERIFY:
    alembic current            → shows 002
    SHOW TABLES;               → course_schedules is GONE
    SELECT * FROM alembic_version; → shows 002

──────────────────────────────────────────────────────────────────────────────
STEP 106 — Rollback ALL migrations (to base):

  COMMAND:
    alembic downgrade base

  EXPECTED OUTPUT:
    INFO  [alembic.runtime.migration] Running downgrade 002 -> 001, add is_active to students
    INFO  [alembic.runtime.migration] Running downgrade 001 -> , initial schema

  VERIFY:
    SHOW TABLES;
    → Only alembic_version remains. All 5 tables are GONE.

    alembic current
    → (no output — no migrations applied)

──────────────────────────────────────────────────────────────────────────────
STEP 107 — Re-apply all migrations:

  COMMAND:
    alembic upgrade head

  EXPECTED OUTPUT:
    INFO  [alembic.runtime.migration] Running upgrade  -> 001, initial schema
    INFO  [alembic.runtime.migration] Running upgrade 001 -> 002, add is_active to students
    INFO  [alembic.runtime.migration] Running upgrade 002 -> 003, add course_schedules table

  VERIFY:
    alembic current
    → 003 (head)     ← back to latest state ✓

    SHOW TABLES;
    → departments, students, courses, enrollments, professors, course_schedules ✓

    DESCRIBE students;
    → is_active column is BACK ✓

──────────────────────────────────────────────────────────────────────────────

SUMMARY OF ALL COMMANDS IN ORDER:
──────────────────────────────────────────────────────────────────────────────
Task 1:
  alembic upgrade 001         ← apply initial schema
  alembic current             ← verify: shows 001 (head)

Task 2:
  alembic upgrade 002         ← add is_active column
  alembic upgrade 003         ← add course_schedules table
  alembic history --verbose   ← see all 3 revisions

Task 3:
  alembic current             ← note current head: 003
  alembic downgrade -1        ← rollback: 003 → 002 (course_schedules gone)
  alembic downgrade base      ← rollback: all gone
  alembic upgrade head        ← re-apply: back to 003 (head)
──────────────────────────────────────────────────────────────────────────────
"""

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════╗
║   Hands-On 7 — Migration Command Reference           ║
╠══════════════════════════════════════════════════════╣
║  TASK 1 — Baseline                                   ║
║    alembic upgrade 001                               ║
║    alembic current                                   ║
╠══════════════════════════════════════════════════════╣
║  TASK 2 — Incremental                                ║
║    alembic upgrade 002                               ║
║    alembic upgrade 003                               ║
║    alembic history --verbose                         ║
╠══════════════════════════════════════════════════════╣
║  TASK 3 — Rollback & Recovery                        ║
║    alembic downgrade -1                              ║
║    alembic downgrade base                            ║
║    alembic upgrade head                              ║
╚══════════════════════════════════════════════════════╝
    """)
