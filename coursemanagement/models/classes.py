from django.db import models

from coursemanagement.models.base_model import BaseModel
from coursemanagement.models.teachers import Teacher

class Class (BaseModel):
    title = models.CharField(max_length = 50, blank = False)
    description = models.CharField(max_length = 200, blank = True)
    workload = models.FloatField(null = False, blank = False)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)