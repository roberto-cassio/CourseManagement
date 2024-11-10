from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


from coursemanagement.models.courses import Courses
from coursemanagement.services.soft_delete_service import is_deleted
from coursemanagement.views.base_model_view_set import SoftDeleteModelViewSet
from coursemanagement.serializers.classes_serializer import ClassesSerializer

from ..models.classes import Classes

class ClassesViewSet(SoftDeleteModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer

    '''Garante que uma aula não seja criada para um curso já deletado'''
    def create(self, request):
        courses_id = request.data.get('courses')
        print(courses_id)
        courses = Courses.objects.filter(id=courses_id).first()
        print (courses)
        if courses and is_deleted(courses):
            return Response(
                { "detail": "Não é possível criar uma aula para um curso deletado."}, status=status.HTTP_400_BAD_REQUEST)



