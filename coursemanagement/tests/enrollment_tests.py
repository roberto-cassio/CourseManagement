import pytest
import time
from django.forms import ValidationError

from coursemanagement.models.students import Student
from coursemanagement.models.courses import Courses
from coursemanagement.models.teachers import Teacher
from coursemanagement.services.enrollment_service import enroll_student, cancel_registration

'''Funções de Auxilio'''
def create_student(name="Estudante Teste", email="teste@exemplo.com"):
    return Student.objects.create(name=name, email=email)

def create_teacher(name="Professor Teste", email="testeprofessor@exemplo.com"):
    return Teacher.objects.create(name=name, email=email)
                               
def create_course(title="Curso Teste", workload = 40, teacher = None):
    if not teacher:
        teacher = create_teacher()
    return Courses.objects.create(title = title, workload= workload, teacher=teacher)

'''
TestCase para verificar se Alunos com Matrícula ativa retornam Flag Correta
'''
@pytest.mark.django_db
def test_enroll_student_successful_registration():
    student = create_student()
    course = create_course()
 
    start_time = time.time()
    registration = enroll_student(student, course)
    duration_ms = (time.time() - start_time) * 1000

    assert registration.student == student
    assert registration.courses == course
    assert registration.enrollment_date is not None
    assert registration.cancellation_date is None
    assert registration.is_active is True
    assert duration_ms < 500, f"A operação levou {duration_ms:.2f}ms, que é mais do que o limite de 500ms"
    

'''
TestCase para verificar o retorno se Aluno já está matrícula no Curso
'''
@pytest.mark.django_db
def test_enroll_student_already_enrolled():
    student = create_student()
    course = create_course()

    enroll_student(student, course)
    
    start_time = time.time()
    with pytest.raises(ValidationError, match="O Aluno já está Matriculado nesse Curso."):
        enroll_student(student, course)
    duration_ms = (time.time() - start_time) * 1000
    assert duration_ms < 500, f"A operação levou {duration_ms:.2f}ms, que é mais do que o limite de 500ms"
'''
TestCase para verificar se Alunos com Matrícula Cancelada retornam Flag Correta
'''

@pytest.mark.django_db
def test_cancel_registration():
    student = create_student()
    course = create_course()

    registration = enroll_student(student, course)
   
    start_time = time.time()
    canceled_registration = cancel_registration(registration.student.id, registration.courses.id)
    duration_ms = (time.time() - start_time) * 1000

    assert canceled_registration.is_active is False
    assert canceled_registration.cancellation_date is not None
    assert duration_ms < 500, f"A operação levou {duration_ms:.2f}ms, que é mais do que o limite de 500ms"

'''
TestCase para verificiar se o cancelamento de uma matrícula já Inativa retorna o erro correto
'''

@pytest.mark.django_db
def test_cancel_registration_inactive():
    student = create_student()
    course = create_course()

    registration = enroll_student(student, course)
    cancel_registration(registration.student.id, registration.courses.id)

    start_time = time.time()
    with pytest.raises(ValidationError, match="Matrícula não encontrada"):
        cancel_registration(registration.student.id, registration.courses.id)
    duration_ms = (time.time() - start_time) * 1000

    
    assert duration_ms < 500, f"A operação levou {duration_ms:.2f}ms, que é mais do que o limite de 500ms"


'''Testcase para verificar se está retornando a exception correta quando uma matrícula inexsitente tenta ser cancelada'''

@pytest.mark.django_db
def test_cancel_registration_not_found():
    student = create_student()
    course = create_course()
    
    start_time = time.time()
    with pytest.raises(ValidationError, match="Matrícula não Encontrada"):
        cancel_registration(student.id, course.id)
    duration_ms = (time.time() - start_time) * 1000
    assert duration_ms < 500, f"A operação levou {duration_ms:.2f}ms, que é mais do que o limite de 500ms"

