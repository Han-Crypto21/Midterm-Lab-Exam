import os, tempfile, json
from src.services.student_service import StudentService
from src.models.student import Student

def test_add_get_update_delete(tmp_path):
    data_file = tmp_path / "students.json"
    data_file.write_text('[]', encoding='utf-8')
    svc = StudentService(str(data_file))
    s = Student(id='S001', first_name='Ana', last_name='Rey', email='ana.rey@example.com', age=20, section='A')
    svc.add_student(s)
    got = svc.get_student('S001')
    assert got is not None and got.email == 'ana.rey@example.com'
    svc.update_student('S001', first_name='Anabelle')
    got2 = svc.get_student('S001')
    assert got2.first_name == 'Anabelle'
    svc.delete_student('S001')
    assert svc.get_student('S001') is None
