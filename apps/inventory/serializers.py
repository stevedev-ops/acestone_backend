from rest_framework import serializers
from .models import JewelleryItem, JewelleryPhoto

class JewelleryPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = JewelleryPhoto
        fields = ['id', 'image', 'caption', 'is_primary']

class JewelleryItemSerializer(serializers.ModelSerializer):
    photos = JewelleryPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = JewelleryItem
        fields = '__all__'

    def to_representation(self, instance):
        """
        Confidentiality Enforcement:
        Strip buying_price and min_selling_price if the requesting user is an employee!
        """
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and hasattr(request, 'user') and request.user.is_authenticated:
            if request.user.role == 'EMPLOYEE':
                data.pop('buying_price', None)
                data.pop('min_selling_price', None)

        return data

