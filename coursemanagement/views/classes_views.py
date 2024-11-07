from ..models.classes import Classes
from coursemanagement.serializers.classes_serializer import ClassesSerializer
from rest_framework import viewsets


class ClassesViewSet(viewsets.ModelViewSet):
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer