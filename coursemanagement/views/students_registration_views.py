from ..models.students_registration import StudentRegistration
from coursemanagement.serializers.students_registration_serializer import StudentRegistrationSerializer
from rest_framework import viewsets


class StudentRegistrationViewSet(viewsets.ModelViewSet):
    queryset = StudentRegistration.objects.all()
    serializer_class = StudentRegistrationSerializer