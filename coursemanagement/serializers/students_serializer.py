from rest_framework import serializers
from coursemanagement.models.students import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'email']