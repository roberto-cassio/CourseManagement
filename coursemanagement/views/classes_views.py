from ..models.classes import Class
from coursemanagement.serializers.classes_serializer import ClassSerializer
from rest_framework import viewsets


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer