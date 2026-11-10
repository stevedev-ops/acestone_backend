from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import JewelleryItem, JewelleryPhoto
from .serializers import JewelleryItemSerializer, JewelleryPhotoSerializer
from apps.accounts.permissions import IsOwnerOrManager, IsOwner

class JewelleryItemViewSet(viewsets.ModelViewSet):
    queryset = JewelleryItem.objects.all()
    serializer_class = JewelleryItemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'name', 'compartment_code', 'purity', 'material']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrManager()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        item = serializer.save()
        # Log product registration audit event
        from apps.audit.models import AuditLog
        AuditLog.objects.create(
            user=self.request.user,
            action='PRODUCT_CREATED',
            entity_type='PRODUCT',
            entity_id=item.code,
            details=f"Registered piece {item.name} ({item.code}) into tray {item.compartment_code}",
            new_value=f"Suggested: KSh {item.suggested_price}"
        )

    @action(detail=False, methods=['get'])
    def in_compartment(self, request):
        code = request.query_params.get('code', '').strip().upper()
        if not code:
            return Response({'error': 'Compartment code is required'}, status=400)
        items = JewelleryItem.objects.filter(compartment_code=code)
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

