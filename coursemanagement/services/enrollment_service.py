from django.forms import ValidationError
from coursemanagement.models.students_registration import StudentRegistration
from django.utils import timezone
from datetime import datetime


def enroll_student(student, course, enrollment_date, cancellation_date):
    '''Aqui fica a lógica de Matrícula do Aluno em um Curso + Validações'''
    if StudentRegistration.objects.filter(student=student, courses=course).exists():
        raise ValidationError("O Aluno já está Matriculado nesse Curso.")
    
    '''Conversão das datas de String para DateTime para fazer as comparações com Dates e adicionando timezone a elas'''
    if isinstance(enrollment_date, str):
        enrollment_date = datetime.fromisoformat(enrollment_date)
        enrollment_date = timezone.make_aware(enrollment_date)

    if cancellation_date and isinstance(cancellation_date, str):
        cancellation_date = datetime.fromisoformat(cancellation_date)
        cancellation_date = timezone.make_aware(cancellation_date)

    '''Levando em conta a data de entrada, e a data de cancelamento, passa um valor para is_active'''
    if enrollment_date <= timezone.now() and (not cancellation_date or cancellation_date > timezone.now()):
        is_active = True
    else:
        is_active = False

    registration = StudentRegistration(student=student, courses=course, enrollment_date = enrollment_date, cancellation_date = cancellation_date, is_active = is_active)
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
        if registration.cancellation_date:
            if registration.enrollment_date > registration.cancellation_date:
                raise ValidationError ("Matrícula não está ativa")
        
        if registration.cancellation_date is None:
            registration.cancellation_date = timezone.now()

        registration.is_active = False
        registration.save()
        return registration
    except StudentRegistration.DoesNotExist:
        raise ValidationError("Matrícula não Encontrada")
