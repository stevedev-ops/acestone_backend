from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from .models import SaleTransaction, SaleItem, ApprovalRequest
from .serializers import SaleTransactionSerializer, ApprovalRequestSerializer
from apps.inventory.models import JewelleryItem
from apps.audit.models import AuditLog

class SaleTransactionViewSet(viewsets.ModelViewSet):
    queryset = SaleTransaction.objects.prefetch_related('items').all()
    serializer_class = SaleTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Employees only view their own sales!
        if user.role == 'EMPLOYEE':
            return self.queryset.filter(employee=user)
        return self.queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Atomic sale checkout with select_for_update locking to prevent duplicate sales.
        """
        data = request.data
        items_data = data.get('items', [])
        if not items_data:
            return Response({'error': 'No items included in transaction'}, status=status.HTTP_400_BAD_REQUEST)

        receipt_number = f"ACE-REC-{timezone.now().year}-{timezone.now().strftime('%m%d%H%M%S')}"
        subtotal = 0
        total_profit = 0
        created_items = []

        # 1. Lock and validate each item
        for item_info in items_data:
            product_id = item_info['product_id']
            negotiated_price = float(item_info['negotiated_price'])

            # Row-level lock
            product = JewelleryItem.objects.select_for_update().get(id=product_id)
            if product.status != JewelleryItem.Status.AVAILABLE or product.quantity < 1:
                return Response(
                    {'error': f"Item {product.code} ({product.name}) is no longer available!"},
                    status=status.HTTP_409_CONFLICT
                )

            # Mark sold
            product.status = JewelleryItem.Status.SOLD
            product.quantity = max(0, product.quantity - 1)
            product.save()

            gross_profit = negotiated_price - float(product.buying_price)
            subtotal += negotiated_price
            total_profit += gross_profit

            created_items.append({
                'product': product,
                'negotiated_price': negotiated_price,
                'gross_profit': gross_profit,
                'buying_cost': product.buying_price,
                'suggested_price': product.suggested_price,
                'approved_by': item_info.get('approved_by', ''),
            })

        amount_paid = float(data.get('amount_paid', subtotal))
        balance_due = max(0.0, subtotal - amount_paid)
        payment_status = SaleTransaction.PaymentStatus.PARTIAL if balance_due > 0 else SaleTransaction.PaymentStatus.COMPLETED

        # 2. Record sale
        sale = SaleTransaction.objects.create(
            receipt_number=receipt_number,
            employee=request.user,
            employee_name=request.user.name,
            subtotal=subtotal,
            discount=float(data.get('discount', 0)),
            total_amount=subtotal,
            total_gross_profit=total_profit,
            payment_method=data.get('payment_method', 'M-Pesa'),
            payment_status=payment_status,
            amount_paid=amount_paid,
            balance_due=balance_due,
            customer_name=data.get('customer_name', ''),
            customer_phone=data.get('customer_phone', ''),
            customer_notes=data.get('customer_notes', ''),
            approved_by=data.get('approved_by', ''),
        )

        for ci in created_items:
            SaleItem.objects.create(
                transaction=sale,
                product=ci['product'],
                product_code=ci['product'].code,
                product_name=ci['product'].name,
                original_buying_cost=ci['buying_cost'],
                suggested_price=ci['suggested_price'],
                negotiated_selling_price=ci['negotiated_price'],
                gross_profit=ci['gross_profit'],
                approved_by=ci['approved_by'],
            )

        # 3. Write immutable audit log
        AuditLog.objects.create(
            user=request.user,
            action='SALE_COMPLETED',
            entity_type='SALE',
            entity_id=receipt_number,
            details=f"Completed sale for {len(created_items)} items via {sale.payment_method}. Total: KSh {sale.total_amount}",
            new_value=f"KSh {sale.total_amount}"
        )

        serializer = self.get_serializer(sale)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def process_return(self, request, pk=None):
        sale = self.get_object()
        if sale.is_returned:
            return Response({'error': 'Sale has already been returned.'}, status=400)

        reason = request.data.get('reason', 'Customer requested return/exchange')
        restore_stock = request.data.get('restore_stock', True)

        with transaction.atomic():
            sale.is_returned = True
            sale.return_reason = reason
            sale.payment_status = SaleTransaction.PaymentStatus.REFUNDED
            sale.save()

            if restore_stock:
                for sale_item in sale.items.all():
                    prod = sale_item.product
                    prod.status = JewelleryItem.Status.AVAILABLE
                    prod.quantity += 1
                    prod.save()

            AuditLog.objects.create(
                user=request.user,
                action='RETURN_PROCESSED',
                entity_type='SALE',
                entity_id=sale.receipt_number,
                details=f"Processed return for receipt {sale.receipt_number}. Reason: {reason}",
            )

        return Response({'status': 'Return processed successfully.'})

class ApprovalRequestViewSet(viewsets.ModelViewSet):
    queryset = ApprovalRequest.objects.all()
    serializer_class = ApprovalRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        if request.user.role not in ['OWNER', 'MANAGER']:
            return Response({'error': 'Only Boss or Manager can authorize price overrides.'}, status=403)

        decision = request.data.get('status', 'APPROVED') # APPROVED or REJECTED
        appr = self.get_object()
        appr.status = decision
        appr.approved_by = f"{request.user.name} ({request.user.get_role_display()})"
        appr.approved_at = timezone.now()
        appr.save()

        AuditLog.objects.create(
            user=request.user,
            action=f"APPROVAL_{decision}",
            entity_type='APPROVAL',
            entity_id=appr.product_code,
            details=f"{decision} discount for {appr.product_name} at KSh {appr.proposed_price}",
        )

        return Response({'status': f"Approval request {decision.lower()}."})

