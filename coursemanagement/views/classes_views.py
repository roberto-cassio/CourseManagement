from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models.classes import Classes
from coursemanagement.serializers.classes_serializer import ClassesSerializer

class ClassesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer


