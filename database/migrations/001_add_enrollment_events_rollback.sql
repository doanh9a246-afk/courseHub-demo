-- Chi dung khi chap nhan mat toan bo lich su su kien.
BEGIN;
DROP TABLE enrollment_events;
DELETE FROM schema_migrations WHERE version = '001';
COMMIT;
