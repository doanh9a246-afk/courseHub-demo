# CourseHub - Buoi 3
Backend: FastAPI + SQLAlchemy Core + PostgreSQL.

Chay tu thu muc goc:
python -m uvicorn backend.app.main:app --reload

Swagger UI: http://127.0.0.1:8000/docs
Postman environment: base_url = http://127.0.0.1:8000

Thu tu kiem tra du lieu:
GET health -> GET courses/sections -> POST enrollment
-> thu loi 409/422 -> DELETE enrollment -> GET sections.

Endpoint:
- GET /health
- GET /courses (q, skip, limit), GET /courses/{course_code}
- GET /lecturers
- GET /sections (available_only), GET /sections/{section_id}
- PATCH /sections/{section_id}/capacity
- GET /students/{student_id}/enrollments
- POST /enrollments, DELETE /enrollments/{student_id}/{class_section_id}

Khong commit backend/.env. Dung backend/.env.example lam mau.
