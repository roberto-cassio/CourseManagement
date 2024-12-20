
from django.db import models

from coursemanagement.models.base_model import BaseModel


class Student (BaseModel):
    name = models.CharField(max_length = 50, blank = False)
    email = models.CharField(max_length = 50, blank = False)
    
    def __str__(self):
        return self.name