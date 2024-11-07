from ..models.teachers import Teacher
from coursemanagement.serializers.teachers_serializer import TeacherSerializer
from rest_framework import viewsets


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer