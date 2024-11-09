from coursemanagement.views.base_model_view_set import SoftDeleteModelViewSet
from ..models.courses import Courses
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from coursemanagement.serializers.courses_serializer import CoursesSerializer

class CoursesViewSet(SoftDeleteModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializer