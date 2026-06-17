CREATE DATABASE college_db;
USE college_db;
CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    hod_name VARCHAR(100),
    budget DECIMAL(12,2)
);
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    department_id INT,
    enrollment_year INT,

    FOREIGN KEY (department_id)
    REFERENCES departments(department_id)
);
CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(20) UNIQUE,
    credits INT,
    department_id INT,

    FOREIGN KEY (department_id)
    REFERENCES departments(department_id)
);
CREATE TABLE enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    grade CHAR(2),

    FOREIGN KEY (student_id)
    REFERENCES students(student_id),

    FOREIGN KEY (course_id)
    REFERENCES courses(course_id)
);
CREATE TABLE professors (
    professor_id INT AUTO_INCREMENT PRIMARY KEY,
    prof_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_id INT,
    salary DECIMAL(10,2),

    FOREIGN KEY (department_id)
    REFERENCES departments(department_id)
);


-- 1NF
-- All columns contain atomic values.
-- Example violation:
-- phone_numbers = '9876543210,8765432109'
-- Multiple values in one column violate 1NF.

-- 2NF
-- All non-key attributes depend on the whole primary key.
-- In enrollments table, grade depends on both student and course.

-- 3NF
-- No transitive dependency exists.
-- Department name is stored in departments table.
-- Students table stores only department_id.
-- Therefore 3NF is satisfied.

-- Enrollments table analysis:
-- enrollment_id is the primary key.
-- grade depends directly on enrollment.
-- No dependency through another non-key column.
-- Therefore enrollments table satisfies 3NF.



ALTER TABLE students
ADD phone_number VARCHAR(15);

ALTER TABLE courses
ADD max_seats INT DEFAULT 60;

ALTER TABLE departments
RENAME COLUMN hod_name TO head_of_dept;

ALTER TABLE students
DROP COLUMN phone_number;