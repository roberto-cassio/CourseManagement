from ..models.courses import Courses
from coursemanagement.serializers.courses_serializer import CoursesSerializer
from rest_framework import viewsets


class CoursesViewSet(viewsets.ModelViewSet):
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializer