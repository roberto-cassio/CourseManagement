from ..models.students import Student
from coursemanagement.serializers.students_serializer import StudentSerializer
from rest_framework import viewsets


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer