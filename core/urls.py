from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def health_check(request):
    return JsonResponse({
        "status": "online",
        "service": "Acestone Jewellery POS & Inventory API",
        "version": "1.0.0",
        "currency": "KES"
    })

urlpatterns = [
    path('', health_check, name='api_root_health'),
    path('health/', health_check, name='api_health'),
    path('admin/', admin.site.urls),
    
    # Auth & Tokens
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Application Routes
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/inventory/', include('apps.inventory.urls')),
    path('api/shelves/', include('apps.shelves.urls')),
    path('api/sales/', include('apps.sales.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/suppliers/', include('apps.suppliers.urls')),
    path('api/expenses/', include('apps.expenses.urls')),
    path('api/reports/', include('apps.reports.urls')),
    path('api/audit/', include('apps.audit.urls')),
]

