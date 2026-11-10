from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Sum, Count
from apps.sales.models import SaleTransaction
from apps.inventory.models import JewelleryItem
from apps.expenses.models import Expense
from apps.accounts.permissions import IsOwner

class FinancialReportView(APIView):
    permission_classes = [IsOwner]

    def get(self, request):
        sales = SaleTransaction.objects.filter(is_returned=False)
        total_revenue = sales.aggregate(val=Sum('total_amount'))['val'] or 0
        total_gross_profit = sales.aggregate(val=Sum('total_gross_profit'))['val'] or 0
        cogs = total_revenue - total_gross_profit

        total_expenses = Expense.objects.aggregate(val=Sum('amount'))['val'] or 0
        net_profit = total_gross_profit - total_expenses

        available_stock = JewelleryItem.objects.filter(status=JewelleryItem.Status.AVAILABLE)
        stock_count = available_stock.count()
        stock_cost = available_stock.aggregate(val=Sum('buying_price'))['val'] or 0
        stock_retail = available_stock.aggregate(val=Sum('suggested_price'))['val'] or 0

        return Response({
            'total_revenue': float(total_revenue),
            'cogs': float(cogs),
            'total_gross_profit': float(total_gross_profit),
            'total_expenses': float(total_expenses),
            'net_profit': float(net_profit),
            'available_pieces_count': stock_count,
            'inventory_purchase_value': float(stock_cost),
            'inventory_retail_potential': float(stock_retail),
        })

