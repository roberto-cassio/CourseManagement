from ..models.teachers import Teacher
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from coursemanagement.serializers.teachers_serializer import TeacherSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer