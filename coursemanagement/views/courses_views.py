from coursemanagement.models.students_registration import StudentRegistration
from coursemanagement.models.teachers import Teacher
from coursemanagement.services.soft_delete_service import is_deleted, delete_course_and_associated_registrations
from coursemanagement.views.base_model_view_set import SoftDeleteModelViewSet
from coursemanagement.serializers.courses_serializer import CoursesSerializer
from ..models.courses import Courses


from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction

class CoursesViewSet(SoftDeleteModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializer

    def destroy (self, request, *args, **kwargs):
        '''Sobrescrever o método destroy do SoftDeleteModelView set para garantir que as matrículas associadas sejam desativadas'''
        course = self.get_object()

        with transaction.atomic():
            #Função responsável por deleção do curso e matrículas associadas
            delete_course_and_associated_registrations(course)

            response = super().destroy(request, *args, **kwargs)

            
        return response
    
    def create (self, request):
        '''Sobrescrever o método create para garantir que não seja criado um curso com um Professor deletado'''
        teacher_id = request.data.get('teacher')

        teacher = Teacher.objects.filter(id=teacher_id).first()
        if teacher and is_deleted(teacher):
            return Response(
                {"detail": "Não é possível criar uma aula para um professor deletado."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            return Response(self.get_serializer(course).data, status=status.HTTP_201_CREATED)