from coursemanagement.views.base_model_view_set import SoftDeleteModelViewSet
from ..models.students import Student
from rest_framework.permissions import IsAuthenticated


from coursemanagement.serializers.students_serializer import StudentSerializer


class StudentViewSet(SoftDeleteModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer