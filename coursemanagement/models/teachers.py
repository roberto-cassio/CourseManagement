
from django.db import models

from coursemanagement.models.base_model import BaseModel


class Teacher (BaseModel):
    name = models.CharField(max_length = 50, blank = False)
    email = models.CharField(max_length = 50, blank = False)