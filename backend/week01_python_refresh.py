students = [
{"id": "24001656", "name": "Nguyen Quoc Doanh", "major": "KHDL"},
{"id": "24001660", "name": "Luong Tien Dung", "major": "KHDL"},
]
courses = [
{
"code": "INT2204",
"name": "Co so du lieu Web va he thong thong tin",
"capacity": 3,
"enrolled": 2,
},
{
"code": "INT2205",
"name": "Khai pha du lieu",
"capacity": 2,
"enrolled": 2,
},
]
enrollments = [
{"student_id": "24001656", "course_code": "INT2204"}
]
for course in courses:
    remaining = course["capacity"] - course["enrolled"]
    print(course["code"], "-con", remaining, "cho")
def find_course(course_code):
    for course in courses:
        if course["code"] == course_code:
            return course
    return None

def find_student(student_id):
    for student in students:
        if student["id"] == student_id:
            return student
    return None

print(find_course("INT2204"))
def can_enroll(student_id, course_code):
    if find_student(student_id) is None:
        return False, "Sinh vien khong ton tai"
    course = find_course(course_code)
    if course is None:
        return False, "Hoc phan khong ton tai"
    duplicated = any(
        item["student_id"] == student_id and item["course_code"] == course_code
        for item in enrollments
    )
    if duplicated:  
        return False, "Sinh vien da dang ky hoc phan nay"
    if course["enrolled"] >= course["capacity"]:
        return False, "Lop da du so luong"
    return True, "Co the dang ky"
print(can_enroll("22000002", "INT2204"))
    
try:
    limit = int(input("Nhap so luong hoc phan muon hien thi: "))
    print(courses[:limit])
except ValueError:
    print("So luong phai la so nguyen")
def search_courses(keyword):
    normalized = keyword.strip().lower()
    results = []
    for course in courses:
        code = course["code"].lower()
        name = course["name"].lower()
        if normalized in code or normalized in name:
            results.append(course)
    return results
print(search_courses("web"))
def enroll_student(student_id, course_code):
    ok, message = can_enroll(student_id, course_code)
    if not ok:
        return False, message
    enrollments.append({"student_id" : student_id, "course_code" : course_code})
    find_course(course_code)["enrolled"] += 1
    return True, "Dang ky thanh cong"

# Kiem tra chuong trinh: 05 tinh huong chay thu
test_cases = [
    ("Dang ky thanh cong", "24001660", "INT2204"),
    ("Dang ky trung", "24001656", "INT2204"),
    ("Lop day", "24001660", "INT2205"),
    ("Ma hoc phan khong ton tai", "24001660", "INT9999"),
    ("Ma sinh vien khong ton tai", "99999999", "INT2204"),
]
for index, (title, student_id, course_code) in enumerate(test_cases, start=1):
    print(f"TC{index} - {title}: {student_id}, {course_code} ->", enroll_student(student_id, course_code))
