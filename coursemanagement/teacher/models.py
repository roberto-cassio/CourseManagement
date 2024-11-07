
from django.db import models

from coursemanagement.common.models import BaseModel


class Teacher (BaseModel):
    name = models.CharField(max_length = 50, blank = False)
    email = models.CharField(max_length = 50, blank = False)