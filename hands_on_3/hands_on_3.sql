SELECT
    s.student_id,
    s.first_name,
    s.last_name,
    COUNT(e.course_id) AS total_courses
FROM students s
JOIN enrollments e
    ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(e.course_id) >
(
    SELECT AVG(course_count)
    FROM
    (
        SELECT COUNT(*) AS course_count
        FROM enrollments
        GROUP BY student_id
    ) avg_table
);

SELECT c.course_name
FROM courses c
WHERE NOT EXISTS
(
    SELECT 1
    FROM enrollments e
    WHERE e.course_id = c.course_id
    AND e.grade <> 'A'
);

SELECT
    d.dept_name,
    p.prof_name,
    p.salary
FROM professors p
JOIN departments d
    ON p.department_id = d.department_id
WHERE p.salary =
(
    SELECT MAX(p2.salary)
    FROM professors p2
    WHERE p2.department_id = p.department_id
);

SELECT *
FROM
(
    SELECT
        d.department_id,
        d.dept_name,
        AVG(p.salary) AS avg_salary
    FROM departments d
    JOIN professors p
        ON d.department_id = p.department_id
    GROUP BY d.department_id, d.dept_name
) dept_avg
WHERE avg_salary > 85000;

CREATE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    CONCAT(s.first_name,' ',s.last_name) AS student_name,
    d.dept_name,

    COUNT(e.course_id) AS total_courses,

    ROUND(
        AVG(
            CASE
                WHEN e.grade='A' THEN 4
                WHEN e.grade='B' THEN 3
                WHEN e.grade='C' THEN 2
                WHEN e.grade='D' THEN 1
                WHEN e.grade='F' THEN 0
            END
        ),2
    ) AS gpa

FROM students s
LEFT JOIN departments d
    ON s.department_id=d.department_id

LEFT JOIN enrollments e
    ON s.student_id=e.student_id

GROUP BY
s.student_id,
student_name,
d.dept_name;

CREATE VIEW vw_course_stats AS
SELECT
    c.course_name,
    c.course_code,

    COUNT(e.student_id) AS total_enrollments,

    ROUND(
        AVG(
            CASE
                WHEN e.grade='A' THEN 4
                WHEN e.grade='B' THEN 3
                WHEN e.grade='C' THEN 2
                WHEN e.grade='D' THEN 1
                WHEN e.grade='F' THEN 0
            END
        ),2
    ) AS avg_gpa

FROM courses c
LEFT JOIN enrollments e
    ON c.course_id=e.course_id

GROUP BY
c.course_id,
c.course_name,
c.course_code;

SELECT *
FROM vw_student_enrollment_summary
WHERE gpa > 3.0;

UPDATE vw_student_enrollment_summary
SET gpa = 4
WHERE student_id = 1;

DROP VIEW IF EXISTS vw_student_enrollment_summary;
DROP VIEW IF EXISTS vw_course_stats;

CREATE VIEW vw_student_enrollment_summary AS
SELECT
    student_id,
    first_name,
    last_name,
    department_id
FROM students
WHERE department_id = 1
WITH CHECK OPTION;

UPDATE vw_student_enrollment_summary
SET department_id = 2
WHERE student_id = 1;

CREATE OR REPLACE FUNCTION fn_enroll_student(
    p_student_id INT,
    p_course_id INT,
    p_enrollment_date DATE
)
RETURNS TEXT
LANGUAGE plpgsql
AS
$$
BEGIN

    IF EXISTS
    (
        SELECT 1
        FROM enrollments
        WHERE student_id = p_student_id
        AND course_id = p_course_id
    )
    THEN
        RAISE EXCEPTION
        'Student already enrolled in this course';
    END IF;

    INSERT INTO enrollments
    (
        student_id,
        course_id,
        enrollment_date
    )
    VALUES
    (
        p_student_id,
        p_course_id,
        p_enrollment_date
    );

    RETURN 'Enrollment Successful';

END;
$$;

SELECT fn_enroll_student(1,3,'2024-01-10');
SELECT fn_enroll_student(1,1,'2024-01-10');

CREATE TABLE department_transfer_log
(
    log_id SERIAL PRIMARY KEY,
    student_id INT,
    old_department INT,
    new_department INT,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

BEGIN;

INSERT INTO enrollments
(student_id,course_id,enrollment_date)
VALUES
(9,1,CURRENT_DATE);

SAVEPOINT first_insert;

INSERT INTO enrollments
(student_id,course_id,enrollment_date)
VALUES
(999,1,CURRENT_DATE);

ROLLBACK TO SAVEPOINT first_insert;

COMMIT;
SELECT *
FROM enrollments
WHERE student_id = 9;