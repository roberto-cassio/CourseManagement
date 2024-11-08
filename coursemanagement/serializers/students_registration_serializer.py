from rest_framework import serializers
from coursemanagement.models.students_registration import StudentRegistration

class StudentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRegistration
        fields = ['student', 'courses']