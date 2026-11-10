from rest_framework import viewsets
from .models import Supplier
from .serializers import SupplierSerializer
from apps.accounts.permissions import IsOwnerOrManager

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsOwnerOrManager]
