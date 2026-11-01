BEGIN;
-- Bang cua migration 001 phai xoa truoc vi co khoa ngoai toi students va class_sections
DROP TABLE IF EXISTS enrollment_events;
DROP TABLE IF EXISTS schema_migrations;
DROP VIEW IF EXISTS v_section_summary;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS class_sections;
DROP TABLE IF EXISTS lecturers;
DROP TABLE IF EXISTS semesters;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;
COMMIT;
