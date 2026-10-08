-- CHI XOA DU LIEU DEMO. Kiem tra SELECT current_database(); truoc khi chay.
BEGIN;
DROP VIEW IF EXISTS v_section_summary;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS class_sections;
DROP TABLE IF EXISTS lecturers;
DROP TABLE IF EXISTS semesters;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;
COMMIT;
