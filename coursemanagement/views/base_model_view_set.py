from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone

from drf_yasg.utils import swagger_auto_schema

class SoftDeleteModelViewSet(viewsets.ModelViewSet):

    '''
    Decidi pela implementação de um sistema de soft delete para evitar a perda de dados sensíveis por erro humano.
    Além disso, manter o registro de matrículas, professores e alunos anteriores é extremamente interessante para uma perspectiva de análise de dados para crescimento
    da plataforma no futuro
    '''
    @swagger_auto_schema(
            operation_description="Realize a deleção lógica do objeto em questão, adicionando um deleted_at com data/hora atual.",            
            responses={
                status.HTTP_204_NO_CONTENT: "Item excluído com sucesso!",
                status.HTTP_400_BAD_REQUEST: "Erro na requisição, dados inválidos.",
            }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Sobrescreve o método destroy para realizar um soft delete,
        marcando o campo 'deleted_at' com a data/hora atual.
        """
        instance = self.get_object()
        instance.deleted_at = timezone.now()
        instance.save() 

        return Response({"message": "Item excluído com sucesso!"}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
            operation_description="Retorna somente com os objetos que não fora deletados lógicamente do sistema.",            
            responses={
                status.HTTP_204_NO_CONTENT: "Sucesso!",
                status.HTTP_400_BAD_REQUEST: "Erro na requisição.",
            }
    )
    def get_queryset(self):
        """
        Sobrescreve o método get_queryset para filtrar os objetos excluídos (soft delete)
        e não retorná-los nas consultas.
        """
        queryset = super().get_queryset()

        return queryset.filter(deleted_at__isnull=True)
