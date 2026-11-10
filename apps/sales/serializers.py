from rest_framework import serializers
from .models import SaleTransaction, SaleItem, ApprovalRequest, NotebookDailySale, DailyRegisterClosing

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = '__all__'

class SaleTransactionSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)

    class Meta:
        model = SaleTransaction
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        # Hide gross profit from employee role
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            if request.user.role == 'EMPLOYEE':
                data.pop('total_gross_profit', None)
        return data

class ApprovalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalRequest
        fields = '__all__'

class NotebookDailySaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotebookDailySale
        fields = '__all__'

class DailyRegisterClosingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyRegisterClosing
        fields = '__all__'

