# CourseHub - Buoi 5: Frontend React ket noi FastAPI

## Thay doi

- `backend/app/main.py`: chi them `CORSMiddleware` (origin `http://localhost:5173`,
  `http://127.0.0.1:5173`; method GET/POST/DELETE; header Content-Type).
  Giu nguyen nghiep vu Buoi 4 (FOR UPDATE, enrollment_events), version 0.4.0.
- `frontend/`: React 18.2.0 + Vite 7.1.7, khong dung thu vien giao dien.
  - `src/api.js`: ham goi API dung chung (xu ly 204, loi 4xx/422, mat ket noi, AbortError).
  - `src/App.jsx`: state, useEffect + AbortController tai `/courses`, `/sections`,
    `/students/{id}/enrollments`; POST/DELETE chi chay tu su kien, sau do luon tai lai tu API.
  - `src/components/`: `Notice`, `SectionTable`, `EnrollmentList`, `StudentForm`.
  - `tests/api.test.mjs`: 8 tinh huong HTTP gia lap cho `api.js`.
- `database/13_week05_verify.sql`: truy van doi chieu (chi doc).
- `.gitignore`: them `.env.local`, `node_modules/`, `dist/`.

## Cach chay

```
# Terminal 1 - thu muc goc
.venv\Scripts\Activate.ps1
python -m uvicorn backend.app.main:app --reload

# Terminal 2 - frontend/
copy .env.example .env.local
npm install
npm run dev        # http://127.0.0.1:5173/
```

## Bai tap tu thuc hanh

- Bai 1: tach form chon sinh vien thanh `StudentForm.jsx`; state van nam o App, truyen qua props.
- Bai 2: them o chon hoc phan (INT2204/INT2205/INT2206) lay tu GET /courses; khong co lop
  phu hop thi hien "Khong co lop phu hop voi bo loc."
- Bai 3: chua lam - Buoi 4 chua co GET /enrollment-events.
- Bai 4: thuoc Project nhom.

## Ket qua kiem tra (Node 24.19.0, PostgreSQL 17)

`npm test`: 8/8 pass. `npm run build`: thanh cong (32 modules).

Truoc bai: `schema_migrations = 001`; WEB-01 capacity 3, enrolled 2, remaining 1;
RACE-01 capacity 1, enrolled 0.

| Kiem tra | Ket qua |
|---|---|
| Preflight OPTIONS /enrollments tu 127.0.0.1:5173 | 200, allow-origin dung, methods GET, POST, DELETE |
| Preflight tu origin la | 400 Disallowed CORS origin |
| GET /students/99999999/enrollments | 404 Khong tim thay sinh vien |
| POST 22000004 / WEB-01 | 201; WEB-01 enrolled 3, remaining 0; them event CREATED (id 100321) |
| POST lap lai | 409 Sinh vien da dang ky lop nay |
| POST thieu class_section_id | 422 Field required |
| DELETE 22000004 / WEB-01 | 204, body rong; WEB-01 ve 2/1; them event CANCELLED (id 100322), CREATED van con |
| RACE-01: 22000002 POST roi 22000004 POST | 201 roi 409; sau do DELETE 22000002 de tra RACE-01 ve 0/1 |

Payload POST trong Network: `{"student_id": "22000004", "class_section_id": "WEB-01"}`.

## Ban phac giao dien (Figma)

Link Figma: _bo sung_ (frame Desktop 1280 px: tieu de, chon sinh vien, danh sach lop,
lop da dang ky; them trang thai dang ky thanh cong va lop het cho).

Khong commit `backend/.env`, `frontend/.env.local`, `node_modules/`, `dist/`.
