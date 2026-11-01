from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import threading

import requests

BASE_URL = "http://127.0.0.1:8000"
SECTION_ID = "RACE-01"
STUDENT_IDS = ["22000002", "22000004"]


def reset_demo() -> None:
    for student_id in STUDENT_IDS:
        response = requests.delete(
            f"{BASE_URL}/enrollments/{student_id}/{SECTION_ID}",
            timeout=10,
        )
        if response.status_code not in (204, 404):
            raise RuntimeError(
                f"Khong reset duoc {student_id}: "
                f"{response.status_code} {response.text}"
            )


def enroll(
    student_id: str,
    barrier: threading.Barrier,
) -> tuple[str, int, object]:
    barrier.wait(timeout=5)
    response = requests.post(
        f"{BASE_URL}/enrollments",
        json={
            "student_id": student_id,
            "class_section_id": SECTION_ID,
        },
        timeout=15,
    )
    body: object = response.json() if response.content else None
    return student_id, response.status_code, body


def set_capacity(capacity: int) -> requests.Response:
    return requests.patch(
        f"{BASE_URL}/sections/{SECTION_ID}/capacity",
        json={"capacity": capacity},
        timeout=15,
    )


def get_race_section() -> dict[str, object]:
    sections = requests.get(f"{BASE_URL}/sections", timeout=5).json()
    return next(
        item for item in sections
        if item["class_id"] == SECTION_ID
    )


def test_post_patch(rounds: int = 20) -> None:
    # Lop co capacity = 2, da co 1 dang ky. POST them 1 sinh vien va PATCH
    # capacity = 1 chay dong thoi: chi duoc 1 request thanh cong.
    for _ in range(rounds):
        reset_demo()
        set_capacity(2).raise_for_status()
        first = requests.post(
            f"{BASE_URL}/enrollments",
            json={"student_id": STUDENT_IDS[1], "class_section_id": SECTION_ID},
            timeout=15,
        )
        assert first.status_code == 201, first.text

        barrier = threading.Barrier(2)

        def patch_capacity() -> int:
            barrier.wait(timeout=5)
            return set_capacity(1).status_code

        with ThreadPoolExecutor(max_workers=2) as executor:
            post_future = executor.submit(enroll, STUDENT_IDS[0], barrier)
            patch_future = executor.submit(patch_capacity)
            post_status = post_future.result()[1]
            patch_status = patch_future.result()

        statuses = sorted([post_status, patch_status])
        assert statuses in ([200, 409], [201, 409]), (
            f"POST {post_status}, PATCH {patch_status}"
        )
        race_section = get_race_section()
        assert race_section["enrolled"] <= race_section["capacity"], race_section

    reset_demo()
    set_capacity(1).raise_for_status()
    print(f"PASS: {rounds} lan POST + PATCH dong thoi, enrolled <= capacity.")


def main() -> None:
    health = requests.get(f"{BASE_URL}/health", timeout=5)
    health.raise_for_status()
    test_post_patch()
    reset_demo()

    barrier = threading.Barrier(len(STUDENT_IDS))
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(enroll, student_id, barrier)
            for student_id in STUDENT_IDS
        ]
        results = [future.result() for future in futures]

    for student_id, status_code, body in results:
        print(student_id, status_code, body)

    statuses = sorted(status_code for _, status_code, _ in results)
    assert statuses == [201, 409], f"Trang thai khong mong doi: {statuses}"

    race_section = get_race_section()
    assert race_section["enrolled"] == 1
    assert race_section["remaining"] == 0
    print("PASS: chi mot request dang ky thanh cong cho lop co 1 cho.")
    print(race_section)


if __name__ == "__main__":
    main()
