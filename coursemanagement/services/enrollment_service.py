from django.forms import ValidationError
from django.utils import timezone

from coursemanagement.models.students_registration import StudentRegistration
from coursemanagement.models.students import Student
from coursemanagement.models.courses import Courses


def enroll_student(student, course):
    '''Aqui fica a lógica de Matrícula do Aluno em um Curso + Validações'''
    #Adicionada validação para checar se o aluno e curso para qual estamos tentando criar a matrícula não estão deletado
    student_exists = Student.objects.filter(id=student.id, deleted_at__isnull = True).exists()
    course_exists = Courses.objects.filter(id=course.id, deleted_at__isnull = True).exists()

    if not student_exists:
        raise ValidationError("Aluno não encontrado.")
    
    if not course_exists:
        raise ValidationError("Curso não encontrado.")

    if StudentRegistration.objects.filter(student=student, courses=course, is_active=True).exists():
        raise ValidationError("O Aluno já está Matriculado nesse Curso.")
    
    is_active = True
    enrollment_date = timezone.now()
    registration = StudentRegistration(student=student, courses=course, enrollment_date = enrollment_date, cancellation_date = None, is_active = is_active)
    registration.full_clean() #Chama a validação antes de salvar
    registration.save()
    return registration

def cancel_registration (student_id, course_id):
    if not student_id or not course_id:
        raise ValidationError("ID do Aluno e ID do Curso são obrigatórios!")
    try:
        registration = StudentRegistration.objects.get(   
            student__id=student_id,
            courses__id=course_id,
            cancellation_date__isnull=True
            )
        
        if not registration.is_active:
            raise ValidationError ("Matrícula não está ativa")
        
        if registration.cancellation_date is None:
            registration.cancellation_date = timezone.now()

        registration.is_active = False
        registration.save()
        return registration
    except StudentRegistration.DoesNotExist:
        raise ValidationError("Matrícula não Encontrada")
