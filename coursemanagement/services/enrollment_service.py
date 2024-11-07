from django.forms import ValidationError
from coursemanagement.models.students_registration import StudentRegistration
from django.utils import timezone
from datetime import datetime


def enroll_student(student, course, enrollment_date, cancellation_date):
    '''Aqui fica a lógica de Matrícula do Aluno em um Curso + Validações'''
    if StudentRegistration.objects.filter(student=student, courses=course).exists():
        raise ValidationError("O Aluno já está Matriculado nesse Curso.")
    
    print (type(cancellation_date))
    '''Conversão das datas de String para DateTime para fazer as checagens'''
    if isinstance(enrollment_date, str):
        enrollment_date = datetime.fromisoformat(enrollment_date)
        enrollment_date = timezone.make_aware(enrollment_date)

    if cancellation_date and isinstance(cancellation_date, str):
        cancellation_date = datetime.fromisoformat(cancellation_date)
        cancellation_date = timezone.make_aware(cancellation_date)


    if enrollment_date <= timezone.now() and (not cancellation_date or cancellation_date > timezone.now()):
        is_active = True
    else:
        is_active = False

    registration = StudentRegistration(student=student, courses=course, enrollment_date = enrollment_date, cancellation_date = cancellation_date, is_active = is_active)
    registration.full_clean() #Chama a validação antes de salvar
    registration.save()
    return registration