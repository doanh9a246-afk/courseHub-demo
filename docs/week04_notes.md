# CourseHub - Buoi 4

- Migration 001: enrollment_events.
- Demo class: RACE-01, capacity = 1.
- POST /enrollments: lock class_sections bang FOR UPDATE.
- Concurrency test: 1 request 201, 1 request 409.
- Performance data: 100000 rows, dataset=performance.
- Index: idx_enrollment_events_dataset_student_time.

## Race condition (2 ket noi doc lap)

| Thi nghiem | Ket qua RACE-01 |
|---|---|
| 09 - khong khoa | capacity = 1, enrolled = 2, remaining = -1 (ca 22000002 va 22000004 deu INSERT) |
| 10 - FOR UPDATE | Tab B cho ~6 giay den khi Tab A COMMIT, doc lai enrolled = 1 roi ROLLBACK; enrolled = 1, remaining = 0 |

## Kiem tra tuan tu qua API (version 0.4.0)

- POST 22000004 vao RACE-01 -> 201 Created
- POST 22000002 vao RACE-01 -> 409 Conflict (Lop hoc phan da het cho)
- DELETE 22000004/RACE-01 -> 204 No Content
- enrollment_events: 1 dong CREATED, 1 dong CANCELLED; enrollments khong con dong RACE-01.

## Concurrency test

Lenh: `python backend/tests/week04_concurrency_test.py` (chay 3 lan, ca 3 lan PASS)

```
22000002 409 {'detail': 'Lop hoc phan da het cho'}
22000004 201 {'message': 'Dang ky thanh cong', 'student_id': '22000004', 'class_section_id': 'RACE-01'}
PASS: chi mot request dang ky thanh cong cho lop co 1 cho.
{'class_id': 'RACE-01', 'course_code': 'INT2204', 'capacity': 1, 'enrolled': 1, 'remaining': 0}
```

## EXPLAIN (ANALYZE, BUFFERS) - 50 su kien gan nhat cua 22000001

Du lieu: 100000 dong dataset = performance. Moi phuong an chay 3 lan tren cung may.

| | Truoc index | Sau index |
|---|---|---|
| Scan type | Seq Scan + Sort (top-N heapsort) | Index Scan using idx_enrollment_events_dataset_student_time |
| Rows Removed by Filter | 99187 | 0 (dung Index Cond) |
| Buffers | shared hit=1140 | shared hit=50 read=3 |
| Execution Time | 8.661 / 10.212 / 8.434 ms | 0.217 / 0.217 / 0.230 ms |

Nhan xet: index (dataset, student_id, occurred_at DESC) cho phep PostgreSQL tim dung vung
dataset + student_id roi doc san theo thu tu occurred_at giam dan, dung sau 50 dong, khong
can doc toan bang va khong can Sort.

## SQL injection

- `GET /courses?q=%25%27%20OR%20%271%27%3D%271%27--` -> 200, `[]` (khong lo toan bo bang).
- `GET /courses` khong co q -> 3 hoc phan.

Khong commit backend/.env.
