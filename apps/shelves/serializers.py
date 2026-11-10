from rest_framework import serializers
from .models import Showcase, ShelfCompartment

class ShelfCompartmentSerializer(serializers.ModelSerializer):
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = ShelfCompartment
        fields = ['id', 'showcase', 'code', 'name', 'capacity', 'items_count']

    def get_items_count(self, obj):
        from apps.inventory.models import JewelleryItem
        return JewelleryItem.objects.filter(compartment_code=obj.code).count()

class ShowcaseSerializer(serializers.ModelSerializer):
    compartments = ShelfCompartmentSerializer(many=True, read_only=True)

    class Meta:
        model = Showcase
        fields = ['id', 'name', 'description', 'compartments']

