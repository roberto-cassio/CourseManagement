from django.db import models

class BaseModel (models.Model):
    deleted_at = models.DateTimeField(blank=True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
