import pytest
from django.forms import ValidationError
from coursemanagement.models.students_registration import StudentRegistration
from coursemanagement.models.students import Student
from coursemanagement.models.courses import Courses
from coursemanagement.models.teachers import Teacher
from coursemanagement.services.enrollment_service import enroll_student, cancel_registration


'''
TestCase para verificar se Alunos com Matrícula ativa retornam Flag Correta
'''
@pytest.mark.django_db
def test_enroll_student_successful_registration():
    student = Student.objects.create(name="Estudante Teste", email="teste@exemplo.com")
    teacher = Teacher.objects.create(name="Professor Teste", email="testeprofessor@exemplo.com")
    course = Courses.objects.create(title="Curso Teste", workload=40, teacher=teacher)

    registration = enroll_student(student, course)

    assert registration.student == student
    assert registration.courses == course
    assert registration.enrollment_date is not None
    assert registration.cancellation_date is None
    assert registration.is_active is True 

'''
TestCase para verificar o retorno se Aluno já está matrícula no Curso
'''
@pytest.mark.django_db
def test_enroll_student_already_enrolled():
    student = Student.objects.create(name="Estudante Teste", email="teste@exemplo.com")
    teacher = Teacher.objects.create(name="Professor Teste", email="testeprofessor@exemplo.com")
    course = Courses.objects.create(title="Curso Teste", workload=40, teacher=teacher)

    enroll_student(student, course)

    with pytest.raises(ValidationError, match="O Aluno já está Matriculado nesse Curso."):
        enroll_student(student, course)

'''
TestCase para verificar se Alunos com Matrícula Cancelada retornam Flag Correta
'''

@pytest.mark.django_db
def test_cancel_registration():
    student = Student.objects.create(name="Estudante Teste", email="teste@exemplo.com")
    teacher = Teacher.objects.create(name="Professor Teste", email="testeprofessor@exemplo.com")
    course = Courses.objects.create(title="Curso Teste", workload=40, teacher=teacher)

    registration = enroll_student(student, course)

    canceled_registration = cancel_registration(registration.student.id, registration.courses.id)

    assert canceled_registration.is_active is False
    assert canceled_registration.cancellation_date is not None

'''
TestCase para verificiar se o cancelamento de uma matrícula já Inativa retorna o erro correto
'''

@pytest.mark.django_db
def test_cancel_registration_inactive():
    student = Student.objects.create(name="Estudante Teste", email="teste@exemplo.com")
    teacher = Teacher.objects.create(name="Professor Teste", email="testeprofessor@exemplo.com")
    course = Courses.objects.create(title="Curso Teste", workload=40, teacher=teacher)

    registration = enroll_student(student, course)
    cancel_registration(registration.student.id, registration.courses.id)

    with pytest.raises(ValidationError, match="Matrícula não está ativa"):
        cancel_registration(registration.student.id, registration.courses.id)

'''Testcase para verificar se está retornando a exception correta quando uma matrícula inexsitente tenta ser cancelada'''

@pytest.mark.django_db
def test_cancel_registration_not_found():
    student = Student.objects.create(name="Estudante Teste", email="teste@exemplo.com")
    teacher = Teacher.objects.create(name="Professor Teste", email="testeprofessor@exemplo.com")
    course = Courses.objects.create(title="Curso Teste", workload=40, teacher=teacher)

    with pytest.raises(ValidationError, match="Matrícula não Encontrada"):
        cancel_registration(student.id, course.id)