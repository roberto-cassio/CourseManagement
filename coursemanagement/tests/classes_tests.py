import pytest
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.utils import timezone

from coursemanagement.models.courses import Courses
from coursemanagement.models.classes import Classes
from coursemanagement.models.teachers import Teacher


@pytest.mark.django_db
def test_class_overlap_validation():
    teacher = Teacher.objects.create(name="Professor Teste", email="professor@exemplo.com")
    course = Courses.objects.create(title="Curso Teste", workload=40, teacher=teacher)
    

    first_class = Classes(
        name="Aula 1 - Python",
        date=timezone.make_aware(datetime(2024, 11, 8, 10, 0)),  # 8 de Novembro, 10:00
        duration=timedelta(hours=1),  # Duração de 1 hora
        courses=course
    )
    first_class.save() 

    overlapping_class = Classes(
        name="Aula 2 - Python",
        date=timezone.make_aware(datetime(2024, 11, 8, 10, 30)),  # 8 de Novembro, 10:30 - sobrepõe a primeira
        duration=timedelta(hours=1),  # Duração de 1 hora
        courses=course
    )

    with pytest.raises(ValidationError, match="Há uma sobreposição de horários com outra aula neste curso."):
        overlapping_class.full_clean() 


    non_overlapping_class = Classes(
        name="Aula 3 - Python",
        date=timezone.make_aware(datetime(2024, 11, 8, 12, 0)),  # 8 de Novembro, 12:00 - sem sobreposição
        duration=timedelta(hours=1),
        courses=course
    )

    non_overlapping_class.full_clean()
    non_overlapping_class.save()  
    assert non_overlapping_class.id is not None  
