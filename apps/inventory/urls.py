from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JewelleryItemViewSet

router = DefaultRouter()
router.register(r'items', JewelleryItemViewSet, basename='jewellery-item')

urlpatterns = [
    path('', include(router.urls)),
]

