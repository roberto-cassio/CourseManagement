from coursemanagement.views.base_model_view_set import SoftDeleteModelViewSet
from ..models.teachers import Teacher

from ..services.soft_delete_service import delete_teacher_and_associated_courses

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from coursemanagement.serializers.teachers_serializer import TeacherSerializer


class TeacherViewSet(SoftDeleteModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    '''Sobrescreve o método destroy, para, na deleção do Professor, também delete o Curso associado a ele. Chamado também o transaction.atomic
    Para garantir que somente uma das operações não seja executada por algum imprevisto causando inconsistência no banco'''
    def destroy(self, request, *args, **kwargs):
        teacher = self.get_object()
        delete_teacher_and_associated_courses(teacher)


        return Response({"message": "Item excluído com sucesso!"}, status=status.HTTP_204_NO_CONTENT)