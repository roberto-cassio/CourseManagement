from ..models.students import Student
from rest_framework import viewsets


from coursemanagement.serializers.students_serializer import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer