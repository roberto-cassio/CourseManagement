from rest_framework import serializers
from coursemanagement.models.teachers import Teacher

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'email']