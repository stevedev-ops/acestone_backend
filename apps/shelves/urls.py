from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShowcaseViewSet, ShelfCompartmentViewSet

router = DefaultRouter()
router.register(r'showcases', ShowcaseViewSet, basename='showcase')
router.register(r'compartments', ShelfCompartmentViewSet, basename='compartment')

urlpatterns = [
    path('', include(router.urls)),
]

