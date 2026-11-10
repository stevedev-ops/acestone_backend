from rest_framework import viewsets, permissions
from .models import Showcase, ShelfCompartment
from .serializers import ShowcaseSerializer, ShelfCompartmentSerializer
from apps.accounts.permissions import IsOwnerOrManager

class ShowcaseViewSet(viewsets.ModelViewSet):
    queryset = Showcase.objects.prefetch_related('compartments').all()
    serializer_class = ShowcaseSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrManager()]
        return [permissions.IsAuthenticated()]

class ShelfCompartmentViewSet(viewsets.ModelViewSet):
    queryset = ShelfCompartment.objects.all()
    serializer_class = ShelfCompartmentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrManager()]
        return [permissions.IsAuthenticated()]

