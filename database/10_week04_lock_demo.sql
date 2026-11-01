-- Lam lai thi nghiem 09 nhung khoa dong class_sections bang FOR UPDATE.
-- Chay lai 08_week04_demo_setup.sql truoc khi bat dau.

-- ===== Tab A: chay toan bo, khi dang pg_sleep(8) thi chuyen sang Tab B =====
BEGIN;
SELECT id, capacity
FROM class_sections
WHERE id = 'RACE-01'
FOR UPDATE;
SELECT COUNT(*) AS enrolled
FROM enrollments
WHERE class_section_id = 'RACE-01';
SELECT pg_sleep(8);
INSERT INTO enrollments (student_id, class_section_id)
VALUES ('22000002', 'RACE-01');
COMMIT;

-- ===== Tab B: chay trong luc Tab A dang pg_sleep =====
-- Lenh FOR UPDATE se cho den khi Tab A COMMIT, sau do COUNT doc duoc enrolled = 1.
-- Khi thay lop da het cho thi ROLLBACK thay vi INSERT.
BEGIN;
SELECT id, capacity
FROM class_sections
WHERE id = 'RACE-01'
FOR UPDATE;
SELECT COUNT(*) AS enrolled
FROM enrollments
WHERE class_section_id = 'RACE-01';
ROLLBACK;

-- ===== Kiem tra: RACE-01 phai co enrolled = 1, remaining = 0 =====
SELECT class_id, capacity, enrolled, remaining
FROM v_section_summary
WHERE class_id = 'RACE-01';
