from django.urls import path
from .views import FinancialReportView

urlpatterns = [
    path('financial-summary/', FinancialReportView.as_view(), name='financial-summary'),
]

