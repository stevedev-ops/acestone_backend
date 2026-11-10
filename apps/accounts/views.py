from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import UserSerializer, VerifyPinSerializer
from .permissions import IsOwner

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['me', 'verify_pin']:
            return [IsAuthenticated()]
        return [IsOwner()]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_pin(self, request):
        serializer = VerifyPinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pin = serializer.validated_data['pin'].strip()

        authorized_user = User.objects.filter(role__in=['OWNER', 'MANAGER'], pin_code=pin).first()
        if authorized_user:
            return Response({
                'valid': True,
                'approver_name': f"{authorized_user.name} ({authorized_user.get_role_display()})",
                'role': authorized_user.role,
            })
        return Response({'valid': False, 'error': 'Invalid PIN.'}, status=status.HTTP_400_BAD_REQUEST)

