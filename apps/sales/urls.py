from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SaleTransactionViewSet, ApprovalRequestViewSet

router = DefaultRouter()
router.register(r'transactions', SaleTransactionViewSet, basename='sale-transaction')
router.register(r'approvals', ApprovalRequestViewSet, basename='approval-request')

urlpatterns = [
    path('', include(router.urls)),
]

