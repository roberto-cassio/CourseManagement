from rest_framework import serializers
from coursemanagement.models.classes import Class

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['title', 'description', 'workload', 'teacher_id']