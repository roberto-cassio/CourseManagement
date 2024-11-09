from rest_framework import viewsets
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

class SoftDeleteModelViewSet(viewsets.ModelViewSet):

    '''
    Decidi pela implementação de um sistema de soft delete para evitar a perda de dados sensíveis por erro humano.
    Além disso, manter o registro de matrículas, professores e alunos anteriores é extremamente interessante para uma perspectiva de análise de dados para crescimento
    da plataforma no futuro
    '''
    
    def destroy(self, request, *args, **kwargs):
        """
        Sobrescreve o método destroy para realizar um soft delete,
        marcando o campo 'deleted_at' com a data/hora atual.
        """
        instance = self.get_object()
        instance.deleted_at = timezone.now()
        instance.save() 

        return Response({"message": "Item excluído com sucesso!"}, status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        """
        Sobrescreve o método get_queryset para filtrar os objetos excluídos (soft delete)
        e não retorná-los nas consultas.
        """
        queryset = super().get_queryset()

        return queryset.filter(deleted_at__isnull=True)
