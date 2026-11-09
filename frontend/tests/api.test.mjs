// Kiem thu api.js voi fetch gia lap (khong goi Backend/PostgreSQL that).
// Chay: npm test (dung trong frontend/)
import { test, afterEach } from "node:test";
import assert from "node:assert/strict";
import { api } from "../src/api.js";

const realFetch = globalThis.fetch;
let calls = [];

function mockFetch(status, bodyText) {
  calls = [];
  globalThis.fetch = async (url, init) => {
    calls.push({ url, init });
    return new Response(bodyText, { status });
  };
}

afterEach(() => {
  globalThis.fetch = realFetch;
});

test("GET 200 tra ve JSON va goi dung URL mac dinh", async () => {
  mockFetch(200, JSON.stringify([{ class_id: "WEB-01", remaining: 1 }]));
  const data = await api("/sections");
  assert.deepEqual(data, [{ class_id: "WEB-01", remaining: 1 }]);
  assert.equal(calls[0].url, "http://127.0.0.1:8000/sections");
  assert.equal(calls[0].init.method, "GET");
  assert.equal(calls[0].init.body, undefined);
  assert.deepEqual(calls[0].init.headers, {});
});

test("POST gui body JSON va header Content-Type", async () => {
  mockFetch(201, JSON.stringify({ message: "Dang ky thanh cong" }));
  const payload = { student_id: "22000004", class_section_id: "WEB-01" };
  const data = await api("/enrollments", { method: "POST", body: payload });
  assert.equal(data.message, "Dang ky thanh cong");
  assert.equal(calls[0].init.method, "POST");
  assert.equal(calls[0].init.headers["Content-Type"], "application/json");
  assert.deepEqual(JSON.parse(calls[0].init.body), payload);
});

test("DELETE 204 tra null, khong doc JSON", async () => {
  mockFetch(204, null);
  const data = await api("/enrollments/22000004/WEB-01", { method: "DELETE" });
  assert.equal(data, null);
});

test("404 nem loi kem detail va status", async () => {
  mockFetch(404, JSON.stringify({ detail: "Khong tim thay sinh vien" }));
  await assert.rejects(api("/students/99999999/enrollments"), (err) => {
    assert.equal(err.status, 404);
    assert.equal(err.message, "HTTP 404: Khong tim thay sinh vien");
    return true;
  });
});

test("409 het cho nem loi kem detail", async () => {
  mockFetch(409, JSON.stringify({ detail: "Lop hoc phan da het cho" }));
  await assert.rejects(
    api("/enrollments", { method: "POST", body: {} }),
    { status: 409, message: "HTTP 409: Lop hoc phan da het cho" },
  );
});

test("422 voi detail dang danh sach duoc ghep thanh chuoi", async () => {
  mockFetch(422, JSON.stringify({
    detail: [{ msg: "Field required" }, { msg: "String should have at least 8 characters" }],
  }));
  await assert.rejects(
    api("/enrollments", { method: "POST", body: {} }),
    { status: 422, message: "HTTP 422: Field required; String should have at least 8 characters" },
  );
});

test("Phan hoi khong phai JSON bao loi ro rang", async () => {
  mockFetch(500, "Internal Server Error");
  await assert.rejects(api("/sections"), { message: "HTTP 500: phản hồi không phải JSON." });
});

test("Mat ket noi bao loi Backend/CORS; AbortError duoc nem lai nguyen ven", async () => {
  globalThis.fetch = async () => { throw new TypeError("Failed to fetch"); };
  await assert.rejects(api("/sections"), /Không nhận được phản hồi API/);

  globalThis.fetch = async () => {
    throw new DOMException("The operation was aborted.", "AbortError");
  };
  await assert.rejects(api("/sections"), { name: "AbortError" });
});
