from coursemanagement.views.base_model_view_set import SoftDeleteModelViewSet
from ..models.teachers import Teacher
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from coursemanagement.serializers.teachers_serializer import TeacherSerializer


class TeacherViewSet(SoftDeleteModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer