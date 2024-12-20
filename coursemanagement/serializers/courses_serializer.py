from rest_framework import serializers
from coursemanagement.models.courses import Courses

class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ['id', 'title', 'description', 'workload', 'teacher']