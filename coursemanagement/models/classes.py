from django.db import models
from django.forms import ValidationError
from django.utils import timezone

from coursemanagement.models.base_model import BaseModel
from coursemanagement.models.courses import Courses

class Classes (BaseModel):
    name = models.CharField(max_length = 50, blank = False)
    topic = models.CharField(max_length = 200, blank = True)
    date = models.DateTimeField(blank = False, null = False)

    '''Optei por adicionar também um campo de Duração de Aulas, afim de evitar conflitos nos Agendamentos'''
    duration = models.DurationField(blank=False, null=False)
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)


    '''Lógica para verificação a aula cadastrada está sobrepondo outra já existente'''
    def clean( self):
        if timezone.is_naive(self.date):
            self.date = timezone.make_aware(self.date)
        
        final_date = self.date + self.duration
        if timezone.is_naive(final_date):
            final_date = timezone.make_aware(final_date)

        overlapping_classes = Classes.objects.filter(courses=self.courses).exclude(id=self.id)

        for existing_class in overlapping_classes:
            existing_end_time = existing_class.date + existing_class.duration
            if (self.date < existing_end_time) and (final_date > existing_class.date):
                raise ValidationError("Há uma sobreposição de horários com outra aula neste curso.")
        
    def __str__(self):
        return self.name