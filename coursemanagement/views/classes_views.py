from rest_framework.permissions import IsAuthenticated

from coursemanagement.views.base_model_view_set import SoftDeleteModelViewSet

from ..models.classes import Classes
from coursemanagement.serializers.classes_serializer import ClassesSerializer

class ClassesViewSet(SoftDeleteModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer



