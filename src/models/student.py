from dataclasses import dataclass, asdict
import re

@dataclass
class Student:
    id: str
    first_name: str
    last_name: str
    email: str
    age: int
    section: str

    def validate(self):
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", self.email):
            raise ValueError(f"Invalid email: {self.email}")
        if not (3 <= self.age <= 120):
            raise ValueError(f"Unreasonable age: {self.age}")

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d: dict):
        return Student(
            id=d["id"],
            first_name=d.get("first_name",""),
            last_name=d.get("last_name",""),
            email=d.get("email",""),
            age=int(d.get("age",0)),
            section=d.get("section","")
        )
