from ..models.students import Student
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


from coursemanagement.serializers.students_serializer import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer