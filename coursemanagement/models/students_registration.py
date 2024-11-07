
from django.db import models
from django.forms import ValidationError

from coursemanagement.models.courses import Courses
from coursemanagement.models.students import Student


class StudentRegistration (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(null = False, blank = False)
    cancellation_date = models.DateTimeField(null = True, blank = True)
    is_active = models.BooleanField()

    def clean(self):
        if self.cancellation_date <= self.enrollment_date:
            raise ValidationError({'cancellation_date': "Data de cancelamento não pode ser anterior a data de entrada"})