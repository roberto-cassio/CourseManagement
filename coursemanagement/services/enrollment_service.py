from django.forms import ValidationError
from coursemanagement.models.students_registration import StudentRegistration
from django.utils import timezone
from datetime import datetime


def enroll_student(student, course):
    '''Aqui fica a lógica de Matrícula do Aluno em um Curso + Validações'''
    if StudentRegistration.objects.filter(student=student, courses=course, is_active=True).exists():
        raise ValidationError("O Aluno já está Matriculado nesse Curso.")
    is_active = True
    enrollment_date = timezone.now()
    registration = StudentRegistration(student=student, courses=course, enrollment_date = enrollment_date, cancellation_date = None, is_active = is_active)
    registration.full_clean() #Chama a validação antes de salvar
    registration.save()
    return registration

def cancel_registration (student_id, course_id):
    try:
        registration = StudentRegistration.objects.get(   
            student__id=student_id,
            courses__id=course_id
            )
        print (registration.student, registration.courses, registration.is_active)
        
        if not registration.is_active:
            raise ValidationError ("Matrícula não está ativa")
        
        if registration.cancellation_date is None:
            registration.cancellation_date = timezone.now()

        registration.is_active = False
        registration.save()
        return registration
    except StudentRegistration.DoesNotExist:
        raise ValidationError("Matrícula não Encontrada")
