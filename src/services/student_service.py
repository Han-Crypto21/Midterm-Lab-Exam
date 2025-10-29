import json, os, tempfile
from typing import List, Optional
from src.models.student import Student

class StudentService:
    def __init__(self, data_path="data/students.json", logger=None):
        self.data_path = data_path
        self.logger = logger
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        if not os.path.exists(self.data_path):
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _read_all(self) -> List[dict]:
        with open(self.data_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_all(self, items: List[dict]):
        # atomic write
        dirn = os.path.dirname(self.data_path) or "."
        fd, tmp = tempfile.mkstemp(dir=dirn)
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=4)
        os.replace(tmp, self.data_path)

    def add_student(self, student: Student):
        student.validate()
        items = self._read_all()
        if any(s["id"] == student.id for s in items):
            raise ValueError("Student with this ID already exists")
        items.append(student.to_dict())
        self._write_all(items)
        if self.logger: self.logger.info(f"Added student {student.id}")

    def get_student(self, student_id: str) -> Optional[Student]:
        items = self._read_all()
        for s in items:
            if s.get("id") == student_id:
                return Student.from_dict(s)
        return None

    def list_students(self) -> List[Student]:
        return [Student.from_dict(s) for s in self._read_all()]

    def update_student(self, student_id: str, **changes):
        items = self._read_all()
        found = False
        for s in items:
            if s.get("id") == student_id:
                s.update(changes)
                found = True
                break
        if not found:
            raise ValueError("Student not found")
        self._write_all(items)
        if self.logger: self.logger.info(f"Updated student {student_id}")

    def delete_student(self, student_id: str):
        items = self._read_all()
        new = [s for s in items if s.get("id") != student_id]
        if len(new) == len(items):
            raise ValueError("Student not found")
        self._write_all(new)
        if self.logger: self.logger.info(f"Deleted student {student_id}")

    def search_students(self, term: str):
        term = term.lower().strip()
        results = []
        for s in self._read_all():
            if term in s.get("first_name","").lower() or term in s.get("last_name","").lower() or term in s.get("id","").lower():
                results.append(Student.from_dict(s))
        return results
