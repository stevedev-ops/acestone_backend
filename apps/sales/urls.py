from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SaleTransactionViewSet, 
    ApprovalRequestViewSet,
    NotebookDailySaleViewSet,
    DailyRegisterClosingViewSet
)

router = DefaultRouter()
router.register(r'transactions', SaleTransactionViewSet, basename='sale-transaction')
router.register(r'approvals', ApprovalRequestViewSet, basename='approval-request')
router.register(r'notebook-sales', NotebookDailySaleViewSet, basename='notebook-sale')
router.register(r'closings', DailyRegisterClosingViewSet, basename='register-closing')

urlpatterns = [
    path('', include(router.urls)),
]

