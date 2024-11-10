from django.db import transaction
from django.utils import timezone

from rest_framework.exceptions import APIException

from coursemanagement.models.courses import Courses
from coursemanagement.models.students_registration import StudentRegistration
from coursemanagement.models.classes import  Classes



class DeletionError(APIException):
    status_code = 500
    default_detail = 'Erro ao deletar o professor e os cursos associados.'
    default_code = 'deletion_error'

def is_deleted(obj):
    return obj.deleted_at is not None


'''
Inicialmente eu estava dando um update com o deleted_at, mas em uma perspectiva de escalabilidade percebi que isso não era muito prático.
Dessa forma, para garantir a consistência entre as deleções, posso chamar o método destroy do próprio Courses, o que acaba gerando o efeito cascata esperado com o soft_delete.
'''


def delete_teacher_and_associated_courses(teacher):
    try:
        with transaction.atomic():
            courses = Courses.objects.filter(teacher=teacher, deleted_at__isnull=True)
            for course in courses:
                delete_course_and_associated_registrations(course)
            teacher.deleted_at = timezone.now()
            teacher.save()
        return True
    except Exception as e:
        raise DeletionError(detail=str(e))

def delete_course_and_associated_registrations(course):
    try:
        course.deleted_at = timezone.now()
        course.save()

        # Marca as matrículas como inativas
        StudentRegistration.objects.filter(courses=course, is_active=True).update(
            is_active=False, cancellation_date=timezone.now()
        )
        
        delete_classes_from_course(course)
    except Exception as e:
        raise DeletionError (detail=f"Erro ao deletar o curso {course.id}: {e}")

def delete_classes_from_course(course):
    '''Deleção das aulas associadas ao curso que está sendo deletado'''
    try:
        classes = Classes.object.filter(courses=course, deleted_at__isnull=True)
        for class_object in classes:
            class_object.deleted_at = timezone.now()
            class_object.save()
    except Exception as e:
        raise DeletionError(detail=f"Erro ao deletar as aulas do course {course.id}: {e}")
