from ..models.teachers import Teacher
from rest_framework import viewsets

from coursemanagement.serializers.teachers_serializer import TeacherSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer