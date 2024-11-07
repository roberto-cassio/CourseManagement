from django.db import models

from coursemanagement.models.base_model import BaseModel
from coursemanagement.models.teachers import Teacher

class Courses (BaseModel):
    title = models.CharField(max_length = 50, blank = False)
    description = models.CharField(max_length = 200, blank = True)
    workload = models.FloatField(null = False, blank = False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.title