-- Chay tung buoc tren cung mot tab Query Tool.

-- Buoc 1
BEGIN;

-- Buoc 2
INSERT INTO enrollments (student_id, class_section_id)
VALUES ('22000004', 'WEB-01');

-- Buoc 3
SELECT class_id, capacity, enrolled, remaining
FROM v_section_summary
WHERE class_id = 'WEB-01';

-- Buoc 4
ROLLBACK;

-- Buoc 5
SELECT class_id, capacity, enrolled, remaining
FROM v_section_summary
WHERE class_id = 'WEB-01';
