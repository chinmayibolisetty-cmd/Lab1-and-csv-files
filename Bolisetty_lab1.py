import csv
import os
import time
import base64
import unittest
import sys


BASE_DIR = os.path.dirname(os.path.abspath("__file__"))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

STUDENTS_FILE   = os.path.join(DATA_DIR, "students.csv")
COURSES_FILE    = os.path.join(DATA_DIR, "courses.csv")
PROFESSORS_FILE = os.path.join(DATA_DIR, "professors.csv")
GRADES_FILE     = os.path.join(DATA_DIR, "grades.csv")
LOGIN_FILE      = os.path.join(DATA_DIR, "login.csv")



#  Password Encryption (Base64 — two-way, encrypt and decrypt)


def encrypt_password(plain_text):
    """Scramble a plain text password into Base64 before saving to file."""
    return base64.b64encode(plain_text.encode("utf-8")).decode("utf-8")

def decrypt_password(encrypted_text):
    """Reverse the Base64 scramble back to the original plain text password."""
    return base64.b64decode(encrypted_text.encode("utf-8")).decode("utf-8")


#  Seed Data — creates the sample CSV files 


def seed_data():
    """Create sample CSV files."""

    # students.csv
    if not os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["email_address","first_name","last_name","course_id","grade","marks"])
            w.writeheader()
            w.writerow({"email_address": "Amber@mycsu.edu", "first_name": "Amber",
                        "last_name": "Jones", "course_id": "DATA200",
                        "grade": "A", "marks": 96})
        print("  Created data/students.csv with sample data.")

    # courses.csv
    if not os.path.exists(COURSES_FILE):
        with open(COURSES_FILE, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["course_id","course_name","description"])
            w.writeheader()
            w.writerow({"course_id": "DATA200", "course_name": "Computer Programming",
                        "description": "Provides insight about DS and Python"})
        print("  Created data/courses.csv with sample data.")

    # professors.csv
    if not os.path.exists(PROFESSORS_FILE):
        with open(PROFESSORS_FILE, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["professor_id","professor_name","rank","course_id"])
            w.writeheader()
            w.writerow({"professor_id": "param@mycsu.edu", "professor_name": "Param Saini",
                        "rank": "Senior Professor", "course_id": "DATA200"})
        print("  Created data/professors.csv with sample data.")

    # login.csv — password stored encrypted
    if not os.path.exists(LOGIN_FILE):
        with open(LOGIN_FILE, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["user_id","password","role"])
            w.writeheader()
    
            w.writerow({"user_id": "param@mycsu.edu",
                        "password": encrypt_password("AQ10134"),
                        "role": "professor"})
            w.writerow({"user_id": "Amber@mycsu.edu",
                        "password": encrypt_password("Welcome12#_"),
                        "role": "student"})
        print("  Created data/login.csv with encrypted passwords.")



#  Student Class
class Student:
    def __init__(self, email_address, first_name, last_name, course_id, grade, marks):
        self.email_address = email_address
        self.first_name    = first_name
        self.last_name     = last_name
        self.course_id     = course_id
        self.grade         = grade
        self.marks         = float(marks)

    def display(self):
        print(f"  {self.first_name} {self.last_name} | "
              f"Email: {self.email_address} | "
              f"Course: {self.course_id} | "
              f"Grade: {self.grade} | Marks: {self.marks}")

    def to_dict(self):
        return {
            "email_address": self.email_address,
            "first_name":    self.first_name,
            "last_name":     self.last_name,
            "course_id":     self.course_id,
            "grade":         self.grade,
            "marks":         self.marks
        }



def load_all_students():
    """Read the students CSV"""
    students = []
    if not os.path.exists(STUDENTS_FILE):
        return students
    with open(STUDENTS_FILE, newline="") as f:
        for row in csv.DictReader(f):
            students.append(Student(
                row["email_address"], row["first_name"], row["last_name"],
                row["course_id"], row["grade"], row["marks"]
            ))
    return students


def save_all_students(students):
    """Write a list of Student objects to the students CSV."""
    fields = ["email_address", "first_name", "last_name", "course_id", "grade", "marks"]
    with open(STUDENTS_FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for s in students:
            w.writerow(s.to_dict())


def display_records():
    """Display all student records to the screen."""
    students = load_all_students()
    if not students:
        print("  No student records found.")
        return
    print(f"\n  {'NAME':<22} {'EMAIL':<28} {'COURSE':<10} {'GRADE':<6} {'MARKS'}")
    for s in students:
        name = s.first_name + " " + s.last_name
        print(f"  {name:<22} {s.email_address:<28} {s.course_id:<10} {s.grade:<6} {s.marks}")
    print(f"\n  Total: {len(students)} records")


def add_new_student():
    """Ask the user for details and add a new student."""
    print("\n  Add New Student")
    email    = input("  Email address: ").strip()
    students = load_all_students()
    if any(s.email_address == email for s in students):
        print("  A student with that email already exists.")
        return
    first  = input("  First name: ").strip()
    last   = input("  Last name: ").strip()
    course = input("  Course ID (e.g. DATA200): ").strip().upper()
    marks  = input("  Marks (e.g. 96): ").strip()
    grade  = letter_for_marks(float(marks))
    students.append(Student(email, first, last, course, grade, marks))
    save_all_students(students)
    print(f"  Student '{first} {last}' added. Grade: {grade}")


def delete_student():
    """Remove a student by their email address."""
    print("\n  Delete Student")
    email    = input("  Enter student email to delete: ").strip()
    students = load_all_students()
    new_list = [s for s in students if s.email_address != email]
    if len(new_list) == len(students):
        print("  Student not found.")
    else:
        save_all_students(new_list)
        print("  Student deleted.")


def update_student_record():
    """Update the marks and grade for an existing student."""
    print("\n  Update Student Record")
    email    = input("  Enter student email to update: ").strip()
    students = load_all_students()
    for s in students:
        if s.email_address == email:
            print(f"  Current Grade: {s.grade}  Marks: {s.marks}")
            new_marks = input("  New marks (leave blank to keep current): ").strip()
            if new_marks:
                s.marks = float(new_marks)
                s.grade = letter_for_marks(s.marks)
            save_all_students(students)
            print(f"  Updated. New Grade: {s.grade}  Marks: {s.marks}")
            return
    print("  Student not found.")


def check_my_grades():
    """Let a student search their own grades by email."""
    print("\n  Check My Grades")
    email    = input("  Enter your email: ").strip()
    students = load_all_students()
    found    = [s for s in students if s.email_address == email]
    if not found:
        print("  No records found.")
    else:
        for s in found:
            s.display()


def search_student():
    """Search for a student by email or last name and display how long it took."""
    print("\n  Search Student")
    query    = input("  Enter email or last name: ").strip().lower()
    students = load_all_students()
    start    = time.time()
    results  = [s for s in students
                if query in s.email_address.lower() or query in s.last_name.lower()]
    elapsed  = time.time() - start
    if results:
        for s in results:
            s.display()
    else:
        print("  No matching records found.")
    print(f"  Search completed in {elapsed:.6f} seconds.")


def sort_students(by="marks", order="asc"):
    """Sort and display students by marks or email."""
    students  = load_all_students()
    reverse   = (order == "desc")
    start     = time.time()
    if by == "marks":
        students.sort(key=lambda s: s.marks, reverse=reverse)
    else:
        students.sort(key=lambda s: s.email_address.lower(), reverse=reverse)
    elapsed   = time.time() - start
    direction = "descending" if reverse else "ascending"
    print(f"\n  Sorted by {by} ({direction}):")
    for s in students:
        s.display()
    print(f"  Sort completed in {elapsed:.6f} seconds.")


def course_statistics(course_id):
    """Print the average and median marks for a given course."""
    students     = load_all_students()
    marks        = [s.marks for s in students if s.course_id.upper() == course_id.upper()]
    if not marks:
        print(f"  No students found for course {course_id}.")
        return
    avg          = sum(marks) / len(marks)
    sorted_marks = sorted(marks)
    n            = len(sorted_marks)
    median       = sorted_marks[n // 2] if n % 2 != 0 else (sorted_marks[n // 2 - 1] + sorted_marks[n // 2]) / 2
    print(f"\n  Stats for {course_id.upper()}:")
    print(f"    Students : {n}")
    print(f"    Average  : {avg:.2f}")
    print(f"    Median   : {median:.2f}")

# Course Class
class Course:
    def __init__(self, course_id, course_name, description):
        self.course_id   = course_id
        self.course_name = course_name
        self.description = description

    def display(self):
        print(f"  [{self.course_id}] {self.course_name} — {self.description}")

    def to_dict(self):
        return {
            "course_id":   self.course_id,
            "course_name": self.course_name,
            "description": self.description
        }



def load_all_courses():
    courses = []
    if not os.path.exists(COURSES_FILE):
        return courses
    with open(COURSES_FILE, newline="") as f:
        for row in csv.DictReader(f):
            courses.append(Course(row["course_id"], row["course_name"], row["description"]))
    return courses


def save_all_courses(courses):
    with open(COURSES_FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["course_id", "course_name", "description"])
        w.writeheader()
        for c in courses:
            w.writerow(c.to_dict())


def display_courses():
    courses = load_all_courses()
    if not courses:
        print(" No courses found.")
        return
    print("\n  Available Courses:")
    for c in courses:
        c.display()


def add_new_course():
    print("\n  Add New Course")
    cid     = input("  Course ID (e.g. DATA200): ").strip().upper()
    courses = load_all_courses()
    if any(c.course_id == cid for c in courses):
        print("  Course ID already exists.")
        return
    name = input("  Course name: ").strip()
    desc = input("  Description: ").strip()
    courses.append(Course(cid, name, desc))
    save_all_courses(courses)
    print(f"  Course '{cid}' added.")


def delete_course():
    print("\n  Delete Course")
    cid      = input("  Course ID to delete: ").strip().upper()
    courses  = load_all_courses()
    new_list = [c for c in courses if c.course_id != cid]
    if len(new_list) == len(courses):
        print("  Course not found.")
    else:
        save_all_courses(new_list)
        print("  Course deleted.")


def modify_course():
    print("\n  Modify Course")
    cid     = input("  Course ID to modify: ").strip().upper()
    courses = load_all_courses()
    for c in courses:
        if c.course_id == cid:
            new_name = input(f"  New name (current: {c.course_name}): ").strip()
            new_desc = input(f"  New description (current: {c.description}): ").strip()
            if new_name: c.course_name = new_name
            if new_desc: c.description = new_desc
            save_all_courses(courses)
            print("  Course updated.")
            return
    print("  Course not found.")


# Professor Class
class Professor:
    def __init__(self, professor_id, professor_name, rank, course_id):
        self.professor_id   = professor_id
        self.professor_name = professor_name
        self.rank           = rank
        self.course_id      = course_id

    def display(self):
        print(f"  {self.professor_name} ({self.rank}) | "
              f"Email: {self.professor_id} | Course: {self.course_id}")

    def to_dict(self):
        return {
            "professor_id":   self.professor_id,
            "professor_name": self.professor_name,
            "rank":           self.rank,
            "course_id":      self.course_id
        }



def load_all_professors():
    professors = []
    if not os.path.exists(PROFESSORS_FILE):
        return professors
    with open(PROFESSORS_FILE, newline="") as f:
        for row in csv.DictReader(f):
            professors.append(Professor(
                row["professor_id"], row["professor_name"],
                row["rank"], row["course_id"]
            ))
    return professors


def save_all_professors(professors):
    with open(PROFESSORS_FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["professor_id", "professor_name", "rank", "course_id"])
        w.writeheader()
        for p in professors:
            w.writerow(p.to_dict())


def display_professors():
    professors = load_all_professors()
    if not professors:
        print("  No professors found.")
        return
    print("\n  Professors:")
    for p in professors:
        p.display()


def add_new_professor():
    print("\n  Add New Professor")
    pid        = input("  Professor email (unique ID): ").strip()
    professors = load_all_professors()
    if any(p.professor_id == pid for p in professors):
        print("  Professor already exists.")
        return
    name   = input("  Full name: ").strip()
    rank   = input("  Rank (e.g. Senior Professor): ").strip()
    course = input("  Course ID they teach: ").strip().upper()
    professors.append(Professor(pid, name, rank, course))
    save_all_professors(professors)
    print(f"  Professor '{name}' added.")


def delete_professor():
    print("\n  Delete Professor")
    pid        = input("  Professor email to delete: ").strip()
    professors = load_all_professors()
    new_list   = [p for p in professors if p.professor_id != pid]
    if len(new_list) == len(professors):
        print("  Professor not found.")
    else:
        save_all_professors(new_list)
        print("  Professor deleted.")


def modify_professor():
    print("\n  Modify Professor")
    pid        = input("  Professor email to modify: ").strip()
    professors = load_all_professors()
    for p in professors:
        if p.professor_id == pid:
            new_name   = input(f"  New name (current: {p.professor_name}): ").strip()
            new_rank   = input(f"  New rank (current: {p.rank}): ").strip()
            new_course = input(f"  New course ID (current: {p.course_id}): ").strip().upper()
            if new_name:   p.professor_name = new_name
            if new_rank:   p.rank = new_rank
            if new_course: p.course_id = new_course
            save_all_professors(professors)
            print("  Professor updated.")
            return
    print("  Professor not found.")


def show_course_by_professor():
    print("\n  Courses by Professor")
    pid        = input("  Professor email: ").strip()
    professors = load_all_professors()
    found      = [p for p in professors if p.professor_id == pid]
    if not found:
        print("  Professor not found.")
    else:
        for p in found:
            p.display()


# Grade Class
class Grade:
    def __init__(self, grade_id, grade, min_marks, max_marks):
        self.grade_id  = grade_id
        self.grade     = grade
        self.min_marks = float(min_marks)
        self.max_marks = float(max_marks)

    def display(self):
        print(f"  [{self.grade_id}] Grade {self.grade}: {self.min_marks} – {self.max_marks}")

    def to_dict(self):
        return {
            "grade_id":  self.grade_id,
            "grade":     self.grade,
            "min_marks": self.min_marks,
            "max_marks": self.max_marks
        }


def letter_for_marks(marks):
    """Return the letter grade for a given numeric score."""
    if marks >= 90: return "A"
    if marks >= 80: return "B"
    if marks >= 70: return "C"
    if marks >= 60: return "D"
    return "F"


def load_all_grades():
    grades = []
    if not os.path.exists(GRADES_FILE):
        return grades
    with open(GRADES_FILE, newline="") as f:
        for row in csv.DictReader(f):
            grades.append(Grade(row["grade_id"], row["grade"],
                                row["min_marks"], row["max_marks"]))
    return grades


def save_all_grades(grades):
    with open(GRADES_FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["grade_id", "grade", "min_marks", "max_marks"])
        w.writeheader()
        for g in grades:
            w.writerow(g.to_dict())


def display_grade_report():
    grades = load_all_grades()
    print("\n  Grade Scale:")
    if not grades:
        print("  A: 90-100 | B: 80-89 | C: 70-79 | D: 60-69 | F: 0-59")
        return
    for g in grades:
        g.display()


def add_grade():
    print("\n  Add Grade Entry")
    grades = load_all_grades()
    gid    = str(len(grades) + 1)
    letter = input("  Letter grade (e.g. A): ").strip().upper()
    lo     = input("  Minimum marks: ").strip()
    hi     = input("  Maximum marks: ").strip()
    grades.append(Grade(gid, letter, lo, hi))
    save_all_grades(grades)
    print(f"  Grade '{letter}' added.")


def delete_grade():
    print("\n  Delete Grade Entry")
    letter   = input("  Letter grade to delete: ").strip().upper()
    grades   = load_all_grades()
    new_list = [g for g in grades if g.grade != letter]
    if len(new_list) == len(grades):
        print("  Grade not found.")
    else:
        save_all_grades(new_list)
        print("  Grade deleted.")


def modify_grade():
    print("\n  Modify Grade Entry")
    letter = input("  Letter grade to modify: ").strip().upper()
    grades = load_all_grades()
    for g in grades:
        if g.grade == letter:
            lo = input(f"  New min marks (current: {g.min_marks}): ").strip()
            hi = input(f"  New max marks (current: {g.max_marks}): ").strip()
            if lo: g.min_marks = float(lo)
            if hi: g.max_marks = float(hi)
            save_all_grades(grades)
            print("  Grade updated.")
            return
    print("  Grade not found.")


# Login User Class

class LoginUser:
    def __init__(self, user_id, password, role):
        self.user_id  = user_id
        self.password = password  # stored as a SHA256 hash
        self.role     = role

    def to_dict(self):
        return {
            "user_id":  self.user_id,
            "password": self.password,
            "role":     self.role
        }



def load_all_users():
    """Load users from CSV, decrypting each password as we go."""
    users = []
    if not os.path.exists(LOGIN_FILE):
        return users
    with open(LOGIN_FILE, newline="") as f:
        for row in csv.DictReader(f):
            # Decrypt the password when loading so we can compare it at login
            plain = decrypt_password(row["password"])
            users.append(LoginUser(row["user_id"], plain, row["role"]))
    return users


def save_all_users(users):
    """Save users to CSV, encrypting each password before writing."""
    with open(LOGIN_FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["user_id", "password", "role"])
        w.writeheader()
        for u in users:
            # Encrypt the password before it goes into the file
            w.writerow({
                "user_id":  u.user_id,
                "password": encrypt_password(u.password),
                "role":     u.role
            })


def register_user():
    print("\n  Register User")
    uid   = input("  Email: ").strip()
    users = load_all_users()
    if any(u.user_id == uid for u in users):
        print("  User already exists.")
        return
    pwd  = input("  Password: ").strip()
    role = input("  Role (student/professor/admin): ").strip().lower()
    # Store plain password in memory — save_all_users will encrypt it
    users.append(LoginUser(uid, pwd, role))
    save_all_users(users)
    print("  Registered. Password is encrypted in the file.")


def login():
    print("\n  Login")
    uid   = input("  Email: ").strip()
    pwd   = input("  Password: ").strip()
    users = load_all_users()
    for u in users:
        if u.user_id == uid and u.password == pwd:
            print(f"  Welcome, {uid}! Role: {u.role}")
            return u
    print("  Invalid email or password.")
    return None


def change_password(current_user):
    if not current_user:
        print("  You must be logged in first.")
        return
    print("\n  Change Password")
    old = input("  Current password: ").strip()
    if old != current_user.password:
        print("  Incorrect current password.")
        return
    new   = input("  New password: ").strip()
    users = load_all_users()
    for u in users:
        if u.user_id == current_user.user_id:
            u.password = new
            break
    save_all_users(users)
    current_user.password = new
    print("  Password updated.")


def logout(current_user):
    if current_user:
        print(f"  {current_user.user_id} has been logged out.")
    else:
        print("  No user is currently logged in.")


# Login Menu
current_user = None


def print_banner():
    print("      CheckMyGrade Application")
    print("      San Jose State University - DATA 200")


def main_menu():
    print("\n  Main Menu")
    print("  1. Login / Register")
    print("  2. Student Records")
    print("  3. Course Management")
    print("  4. Professor Management")
    print("  5. Grade Scale")
    print("  6. Search and Sort")
    print("  7. Reports and Statistics")
    print("  0. Exit")
    if current_user:
        print(f"\n  Logged in as: {current_user.user_id} [{current_user.role}]")


def student_menu():
    while True:
        print("\n  Student Records")
        print("  1. Display all students")
        print("  2. Add student")
        print("  3. Delete student")
        print("  4. Update student")
        print("  5. Check my grades")
        print("  0. Back")
        choice = input("  Choice: ").strip()
        if   choice == "1": display_records()
        elif choice == "2": add_new_student()
        elif choice == "3": delete_student()
        elif choice == "4": update_student_record()
        elif choice == "5": check_my_grades()
        elif choice == "0": break
        else: print("  Invalid choice.")


def course_menu():
    while True:
        print("\n  Course Management")
        print("  1. Display all courses")
        print("  2. Add course")
        print("  3. Delete course")
        print("  4. Modify course")
        print("  0. Back")
        choice = input("  Choice: ").strip()
        if   choice == "1": display_courses()
        elif choice == "2": add_new_course()
        elif choice == "3": delete_course()
        elif choice == "4": modify_course()
        elif choice == "0": break
        else: print("  Invalid choice.")


def professor_menu():
    while True:
        print("\n  Professor Management")
        print("  1. Display all professors")
        print("  2. Add professor")
        print("  3. Delete professor")
        print("  4. Modify professor")
        print("  5. Show professor course")
        print("  0. Back")
        choice = input("  Choice: ").strip()
        if   choice == "1": display_professors()
        elif choice == "2": add_new_professor()
        elif choice == "3": delete_professor()
        elif choice == "4": modify_professor()
        elif choice == "5": show_course_by_professor()
        elif choice == "0": break
        else: print("  Invalid choice.")


def grade_menu():
    while True:
        print("\n  Grade Scale")
        print("  1. Display grade scale")
        print("  2. Add grade entry")
        print("  3. Delete grade entry")
        print("  4. Modify grade entry")
        print("  0. Back")
        choice = input("  Choice: ").strip()
        if   choice == "1": display_grade_report()
        elif choice == "2": add_grade()
        elif choice == "3": delete_grade()
        elif choice == "4": modify_grade()
        elif choice == "0": break
        else: print("  Invalid choice.")


def search_sort_menu():
    while True:
        print("\n  Search and Filter")
        print("  1. Search student")
        print("  2. Sort by marks ascending")
        print("  3. Sort by marks descending")
        print("  4. Sort by email ascending")
        print("  0. Back")
        choice = input("  Choice: ").strip()
        if   choice == "1": search_student()
        elif choice == "2": sort_students(by="marks", order="asc")
        elif choice == "3": sort_students(by="marks", order="desc")
        elif choice == "4": sort_students(by="email", order="asc")
        elif choice == "0": break
        else: print("  Invalid choice.")


def reports_menu():
    while True:
        print("\n  Reports and Statistics")
        print("  1. Course statistics")
        print("  2. Display grade scale")
        print("  0. Back")
        choice = input("  Choice: ").strip()
        if   choice == "1":
            cid = input("  Enter course ID: ").strip()
            course_statistics(cid)
        elif choice == "2": display_grade_report()
        elif choice == "0": break
        else: print("  Invalid choice.")


def account_menu():
    global current_user
    while True:
        print("\n  Account")
        print("  1. Login")
        print("  2. Register")
        print("  3. Change password")
        print("  4. Logout")
        print("  0. Back")
        choice = input("  Choice: ").strip()
        if   choice == "1": current_user = login()
        elif choice == "2": register_user()
        elif choice == "3": change_password(current_user)
        elif choice == "4":
            logout(current_user)
            current_user = None
        elif choice == "0": break
        else: print("  Invalid choice.")


def main():
    print_banner()
    seed_data()   # create sample CSV files if they don't exist yet
    while True:
        main_menu()
        choice = input("\n  Enter choice: ").strip()
        if   choice == "1": account_menu()
        elif choice == "2": student_menu()
        elif choice == "3": course_menu()
        elif choice == "4": professor_menu()
        elif choice == "5": grade_menu()
        elif choice == "6": search_sort_menu()
        elif choice == "7": reports_menu()
        elif choice == "0":
            print("\n  Goodbye!\n")
            break
        else:
            print("  Invalid choice. Please try again.")



#  Unit Tests
class TestStudentRecords(unittest.TestCase):

    def setUp(self):
        if os.path.exists(STUDENTS_FILE): os.remove(STUDENTS_FILE)

    def tearDown(self):
        if os.path.exists(STUDENTS_FILE): os.remove(STUDENTS_FILE)

    def test_add_student(self):
        s = Student("alice@test.edu", "Alice", "Smith", "DATA200", "A", 95)
        save_all_students([s])
        loaded = load_all_students()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].email_address, "alice@test.edu")

    def test_delete_student(self):
        save_all_students([
            Student("a@test.edu", "A", "B", "DATA200", "A", 95),
            Student("b@test.edu", "C", "D", "DATA200", "B", 83)
        ])
        remaining = [s for s in load_all_students() if s.email_address != "a@test.edu"]
        save_all_students(remaining)
        self.assertEqual(len(load_all_students()), 1)

    def test_modify_student(self):
        save_all_students([Student("a@test.edu", "A", "B", "DATA200", "A", 95)])
        loaded = load_all_students()
        loaded[0].marks = 99.0
        save_all_students(loaded)
        self.assertEqual(load_all_students()[0].marks, 99.0)

    def test_bulk_1000_records(self):
        bulk = [Student(f"s{i}@test.edu", "F", "L", "DATA200", "B", 60 + (i % 40))
                for i in range(1000)]
        save_all_students(bulk)
        self.assertEqual(len(load_all_students()), 1000)

    def test_search_timing(self):
        save_all_students([Student(f"s{i}@test.edu", "F", "L", "DATA200", "B", 75)
                           for i in range(1000)])
        loaded  = load_all_students()
        start   = time.time()
        results = [s for s in loaded if "s500" in s.email_address]
        elapsed = time.time() - start
        self.assertGreater(len(results), 0)
        print(f"\n    Search: {len(results)} result(s) in {elapsed:.6f}s")

    def test_sort_marks_ascending(self):
        save_all_students([Student(f"s{i}@test.edu", "F", "L", "DATA200", "B", 100 - i)
                           for i in range(1000)])
        loaded  = load_all_students()
        start   = time.time()
        sorted_ = sorted(loaded, key=lambda s: s.marks)
        elapsed = time.time() - start
        self.assertLessEqual(sorted_[0].marks, sorted_[-1].marks)
        print(f"\n    Sort ascending: 1000 records in {elapsed:.6f}s")

    def test_sort_marks_descending(self):
        save_all_students([Student(f"s{i}@test.edu", "F", "L", "DATA200", "B", i)
                           for i in range(1000)])
        loaded  = load_all_students()
        start   = time.time()
        sorted_ = sorted(loaded, key=lambda s: s.marks, reverse=True)
        elapsed = time.time() - start
        self.assertGreaterEqual(sorted_[0].marks, sorted_[-1].marks)
        print(f"\n    Sort descending: 1000 records in {elapsed:.6f}s")

    def test_sort_by_email(self):
        save_all_students([Student(f"s{i:04d}@test.edu", "F", "L", "DATA200", "B", 75)
                           for i in range(100)])
        loaded  = load_all_students()
        start   = time.time()
        sorted_ = sorted(loaded, key=lambda s: s.email_address.lower())
        elapsed = time.time() - start
        self.assertLessEqual(sorted_[0].email_address, sorted_[-1].email_address)
        print(f"\n    Sort by email: 100 records in {elapsed:.6f}s")


class TestCourseRecords(unittest.TestCase):

    def setUp(self):
        if os.path.exists(COURSES_FILE): os.remove(COURSES_FILE)

    def tearDown(self):
        if os.path.exists(COURSES_FILE): os.remove(COURSES_FILE)

    def test_add_course(self):
        save_all_courses([Course("DATA200", "Data Science", "Intro to DS")])
        self.assertEqual(load_all_courses()[0].course_id, "DATA200")

    def test_delete_course(self):
        save_all_courses([Course("DATA200", "DS", "desc"), Course("CS101", "CS", "desc")])
        remaining = [c for c in load_all_courses() if c.course_id != "CS101"]
        save_all_courses(remaining)
        self.assertEqual(len(load_all_courses()), 1)

    def test_modify_course(self):
        save_all_courses([Course("DATA200", "DS", "Old desc")])
        loaded = load_all_courses()
        loaded[0].description = "New desc"
        save_all_courses(loaded)
        self.assertEqual(load_all_courses()[0].description, "New desc")


class TestProfessorRecords(unittest.TestCase):

    def setUp(self):
        if os.path.exists(PROFESSORS_FILE): os.remove(PROFESSORS_FILE)

    def tearDown(self):
        if os.path.exists(PROFESSORS_FILE): os.remove(PROFESSORS_FILE)

    def test_add_professor(self):
        save_all_professors([Professor("p@test.edu", "Dr. Smith", "Senior Professor", "DATA200")])
        self.assertEqual(load_all_professors()[0].professor_id, "p@test.edu")

    def test_delete_professor(self):
        save_all_professors([
            Professor("a@test.edu", "Dr. A", "Professor", "DATA200"),
            Professor("b@test.edu", "Dr. B", "Lecturer",  "CS101")
        ])
        remaining = [p for p in load_all_professors() if p.professor_id != "b@test.edu"]
        save_all_professors(remaining)
        self.assertEqual(len(load_all_professors()), 1)

    def test_modify_professor(self):
        save_all_professors([Professor("p@test.edu", "Dr. Old", "Lecturer", "DATA200")])
        loaded = load_all_professors()
        loaded[0].rank = "Senior Professor"
        save_all_professors(loaded)
        self.assertEqual(load_all_professors()[0].rank, "Senior Professor")


class TestGradeLogic(unittest.TestCase):

    def test_grade_boundaries(self):
        self.assertEqual(letter_for_marks(95), "A")
        self.assertEqual(letter_for_marks(85), "B")
        self.assertEqual(letter_for_marks(75), "C")
        self.assertEqual(letter_for_marks(65), "D")
        self.assertEqual(letter_for_marks(50), "F")


class TestLoginUser(unittest.TestCase):

    def setUp(self):
        if os.path.exists(LOGIN_FILE): os.remove(LOGIN_FILE)

    def tearDown(self):
        if os.path.exists(LOGIN_FILE): os.remove(LOGIN_FILE)

    def test_encrypt_decrypt_roundtrip(self):
        """Encrypting then decrypting should give back the original password."""
        plain     = "Welcome12#_"
        encrypted = encrypt_password(plain)
        self.assertNotEqual(plain, encrypted)        
        self.assertEqual(decrypt_password(encrypted), plain) 

    def test_password_not_visible_in_file(self):
        """The plain text password is not visible in the csv file."""
        save_all_users([LoginUser("u@test.edu", "Secret123", "student")])
        with open(LOGIN_FILE) as f:
            raw = f.read()
        self.assertNotIn("Secret123", raw)  

    def test_login_works_after_encrypt(self):
        """A user saved with an encrypted password is able to log in."""
        save_all_users([LoginUser("u@test.edu", "mypassword", "student")])
        users = load_all_users()
        self.assertEqual(users[0].password, "mypassword")  

    def test_sample_passwords_from_assignment(self):
        """Verify the sample data."""
        save_all_users([
            LoginUser("micheal@mycsu.edu", "AQ10134",     "professor"),
            LoginUser("sam@mycsu.edu",     "Welcome12#_", "student")
        ])
        users = load_all_users()
        self.assertEqual(users[0].password, "AQ10134")
        self.assertEqual(users[1].password, "Welcome12#_")


# Start Point

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        sys.argv.pop(1)
        unittest.main()
    else:
        main()

import unittest

loader = unittest.TestLoader()
suite  = unittest.TestSuite()

suite.addTests(loader.loadTestsFromTestCase(TestStudentRecords))
suite.addTests(loader.loadTestsFromTestCase(TestCourseRecords))
suite.addTests(loader.loadTestsFromTestCase(TestProfessorRecords))
suite.addTests(loader.loadTestsFromTestCase(TestGradeLogic))
suite.addTests(loader.loadTestsFromTestCase(TestLoginUser))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
