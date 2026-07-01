# models.py
# Hands-On 6 — Database Integration (No SQLAlchemy)
# Uses: mysql-connector-python
# Install: pip install mysql-connector-python

import mysql.connector
from mysql.connector import Error

# ─── Database Configuration ───────────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",         # 🔁 Change to your MySQL username
    "password": "yourpassword", # 🔁 Change to your MySQL password
    "database": "college_db_orm"
}

# ─── Connection Helper ────────────────────────────────────────────────────────
def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"❌ Connection failed: {e}")
        return None


# ─── Create Database ──────────────────────────────────────────────────────────
def create_database():
    try:
        # Connect without specifying database first
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS college_db_orm")
        print("✅ Database 'college_db_orm' created (or already exists).")
        cursor.close()
        conn.close()
    except Error as e:
        print(f"❌ Error creating database: {e}")


# ─── Create All Tables ────────────────────────────────────────────────────────
def create_tables():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()

    # 1. departments (create first — others reference it)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            department_id INT AUTO_INCREMENT PRIMARY KEY,
            dept_name     VARCHAR(100) NOT NULL,
            head_of_dept  VARCHAR(100),
            budget        DECIMAL(12,2)
        )
    """)
    print("✅ Table 'departments' ready.")

    # 2. students
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id      INT AUTO_INCREMENT PRIMARY KEY,
            first_name      VARCHAR(50)  NOT NULL,
            last_name       VARCHAR(50)  NOT NULL,
            email           VARCHAR(100) NOT NULL UNIQUE,
            date_of_birth   DATE,
            department_id   INT,
            enrollment_year INT,
            FOREIGN KEY (department_id) REFERENCES departments(department_id)
        )
    """)
    print("✅ Table 'students' ready.")

    # 3. courses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id     INT AUTO_INCREMENT PRIMARY KEY,
            course_name   VARCHAR(150) NOT NULL,
            course_code   VARCHAR(20)  UNIQUE,
            credits       INT,
            department_id INT,
            max_seats     INT DEFAULT 60,
            FOREIGN KEY (department_id) REFERENCES departments(department_id)
        )
    """)
    print("✅ Table 'courses' ready.")

    # 4. enrollments
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id   INT AUTO_INCREMENT PRIMARY KEY,
            student_id      INT,
            course_id       INT,
            enrollment_date DATE,
            grade           CHAR(2),
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (course_id)  REFERENCES courses(course_id)
        )
    """)
    print("✅ Table 'enrollments' ready.")

    # 5. professors
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professors (
            professor_id  INT AUTO_INCREMENT PRIMARY KEY,
            prof_name     VARCHAR(100) NOT NULL,
            email         VARCHAR(100) UNIQUE,
            department_id INT,
            salary        DECIMAL(10,2),
            FOREIGN KEY (department_id) REFERENCES departments(department_id)
        )
    """)
    print("✅ Table 'professors' ready.")

    conn.commit()
    cursor.close()
    conn.close()
    print("\n✅ All 5 tables created in college_db_orm successfully.")


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  Hands-On 6 — models.py (No SQLAlchemy)")
    print("=" * 50)
    create_database()
    create_tables()