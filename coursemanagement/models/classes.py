from django.db import models

from coursemanagement.models.base_model import BaseModel
from coursemanagement.models.courses import Courses

class Classes (BaseModel):
    name = models.CharField(max_length = 50, blank = False)
    topic = models.CharField(max_length = 200, blank = True)
    date = models.DateTimeField(blank = False, null = False)
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)


    def __str__(self):
        return self.name