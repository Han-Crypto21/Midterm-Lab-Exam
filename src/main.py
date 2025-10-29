import sys
from src.utils.config_loader import load_config
from src.utils.logger import get_logger
from src.services.student_service import StudentService
from src.models.student import Student

def print_menu():
    print("\nStudent Info System\nCommands:")
    print("1. Add student")
    print("2. List students")
    print("3. View student")
    print("4. Update student")
    print("5. Delete student")
    print("6. Search students")
    print("0. Exit")

def input_student():
    sid = input("ID: ").strip()
    fn = input("First name: ").strip()
    ln = input("Last name: ").strip()
    email = input("Email: ").strip()
    age = int(input("Age: ").strip() or 0)
    section = input("Section: ").strip()
    return Student(id=sid, first_name=fn, last_name=ln, email=email, age=age, section=section)

def main():
    cfg = load_config()
    logger = get_logger(cfg.get("app_name"), cfg.get("log_path","logs/app.log"))
    svc = StudentService(cfg.get("data_path","data/students.json"), logger=logger)
    while True:
        print_menu()
        cmd = input("Choose: ").strip()
        try:
            if cmd == "1" or cmd.lower() == "add":
                s = input_student()
                svc.add_student(s)
                print("Student added.")
            elif cmd == "2" or cmd.lower() == "list":
                for s in svc.list_students():
                    print(s.to_dict())
            elif cmd == "3" or cmd.lower() == "view":
                sid = input("Student ID: ").strip()
                s = svc.get_student(sid)
                print(s.to_dict() if s else "Not found")
            elif cmd == "4" or cmd.lower() == "update":
                sid = input("Student ID to update: ").strip()
                print("Enter fields to update (leave blank to skip)")
                changes = {}
                fn = input("First name: ").strip()
                if fn: changes["first_name"] = fn
                ln = input("Last name: ").strip()
                if ln: changes["last_name"] = ln
                email = input("Email: ").strip()
                if email: changes["email"] = email
                age = input("Age: ").strip()
                if age: changes["age"] = int(age)
                section = input("Section: ").strip()
                if section: changes["section"] = section
                svc.update_student(sid, **changes)
                print("Updated.")
            elif cmd == "5" or cmd.lower() == "delete":
                sid = input("Student ID to delete: ").strip()
                svc.delete_student(sid)
                print("Deleted.")
            elif cmd == "6" or cmd.lower() == "search":
                term = input("Search term: ").strip()
                for s in svc.search_students(term):
                    print(s.to_dict())
            elif cmd == "0" or cmd.lower() == "exit":
                print("Goodbye"); sys.exit(0)
            else:
                print("Unknown command") 
        except Exception as e:
            logger.exception(e)
            print("Error:", e)

if __name__ == "__main__":
    main()
