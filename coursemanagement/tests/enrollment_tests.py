import pytest
from django.forms import ValidationError
from coursemanagement.models.students_registration import StudentRegistration
from coursemanagement.models.students import Student
from coursemanagement.models.courses import Courses
from coursemanagement.models.teachers import Teacher
from coursemanagement.services.enrollment_service import enroll_student, cancel_registration
from django.utils import timezone
'''
TestCase para verificar se Alunos com Matrícula ativa retornam Flag Correta
'''

@pytest.mark.django_db
def test_enroll_student_successful_registration():
    student = Student.objects.create(name="Estudante Teste", email="teste@exemplo.com")
    teacher = Teacher.objects.create(name="Professor Teste", email="testeprofessor@exemplo.com")
    course = Courses.objects.create(title="Curso Teste", workload=40, teacher=teacher)
    enrollment_date = timezone.now()
    cancellation_date = None

    registration = enroll_student(student, course, enrollment_date, cancellation_date)

    assert registration.student == student
    assert registration.courses == course
    assert registration.enrollment_date == enrollment_date
    assert registration.cancellation_date == cancellation_date
    assert registration.is_active is True

'''
TestCase para verificar o retorno se Aluno já está matrícula no Curso
'''
@pytest.mark.django_db
def test_enroll_student_already_enrolled():
    student = Student.objects.create(name="Estudante Teste", email="teste@exemplo.com")
    teacher = Teacher.objects.create(name="Professor Teste", email="testeprofessor@exemplo.com")
    course = Courses.objects.create(title="Curso Teste", workload=40, teacher=teacher)
    enrollment_date = timezone.now()
    cancellation_date = None

    StudentRegistration.objects.create(student=student, courses=course, enrollment_date=enrollment_date, is_active=True)

    with pytest.raises(ValidationError, match="O Aluno já está Matriculado nesse Curso."):
        enroll_student(student, course, enrollment_date, cancellation_date)

'''
TestCase para verificar se Alunos com Matrícula Cancelada retornam Flag Correta
'''

@pytest.mark.django_db
def test_enroll_student_with_past_cancellation_date():
    student = Student.objects.create(name="Estudante Teste", email="teste@exemplo.com")
    teacher = Teacher.objects.create(name="Professor Teste", email="testeprofessor@exemplo.com")
    course = Courses.objects.create(title="Curso Teste", workload=40, teacher=teacher)
    enrollment_date = timezone.now() - timezone.timedelta(days=2)
    cancellation_date = timezone.now() - timezone.timedelta(days=1)  # Data passada

    registration = enroll_student(student, course, enrollment_date, cancellation_date)

    assert registration.is_active is False

'''
TestCase para verificar se Alunos com Matrícula ativa retornam Flag Correta
'''

@pytest.mark.django_db
def test_enroll_student_with_future_enrollment_date():
    student = Student.objects.create(name="Estudante Teste", email="teste@exemplo.com")
    teacher = Teacher.objects.create(name="Professor Teste", email="testeprofessor@exemplo.com")
    course = Courses.objects.create(title="Curso Teste", workload=40, teacher=teacher)
    enrollment_date = timezone.now() + timezone.timedelta(days=1)  # Data futura
    cancellation_date = None

    registration = enroll_student(student, course, enrollment_date, cancellation_date)

    assert registration.is_active is False


@pytest.mark.django_db
def test_cancel_registration():
    student = Student.objects.create(name="Estudante Teste", email="teste@exemplo.com")
    teacher = Teacher.objects.create(name="Professor Teste", email="testeprofessor@exemplo.com")
    course = Courses.objects.create(title="Curso Teste", workload=40, teacher=teacher)
    enrollment_date = timezone.now()
    registration = StudentRegistration.objects.create(
        student=student,
        courses=course,
        enrollment_date=enrollment_date,
        is_active=True
    )

    # Tenta cancelar a matrícula
    canceled_registration = cancel_registration(registration.student.name, registration.courses.title)

    # Verifica se a matrícula foi cancelada corretamente
    assert canceled_registration.is_active is False
    assert canceled_registration.cancellation_date is not None