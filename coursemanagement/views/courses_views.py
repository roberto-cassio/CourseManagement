from ..models.courses import Courses
from rest_framework import viewsets

from coursemanagement.serializers.courses_serializer import CoursesSerializer

class CoursesViewSet(viewsets.ModelViewSet):
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializer