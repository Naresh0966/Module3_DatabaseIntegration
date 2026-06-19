EXPLAIN
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

CREATE INDEX idx_students_enrollment_year
ON students(enrollment_year);

CREATE UNIQUE INDEX idx_enrollments_student_course
ON enrollments(student_id, course_id);

CREATE INDEX idx_courses_course_code
ON courses(course_code);

EXPLAIN
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

CREATE INDEX idx_enrollments_null_grade
ON enrollments(student_id)
WHERE grade IS NULL;

EXPLAIN
SELECT *
FROM enrollments
WHERE grade IS NULL;

EXPLAIN ANALYZE
SELECT *
FROM students
WHERE enrollment_year = 2022;

EXPLAIN ANALYZE
SELECT *
FROM courses
WHERE course_code = 'CS101';

EXPLAIN ANALYZE
SELECT *
FROM enrollments
WHERE student_id = 1
AND course_id = 1;