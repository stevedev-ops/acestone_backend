from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.shelves.models import Showcase, ShelfCompartment
from apps.suppliers.models import Supplier
from apps.inventory.models import JewelleryItem
from apps.sales.models import SaleTransaction, SaleItem, NotebookDailySale
from apps.expenses.models import Expense
from apps.audit.models import AuditLog

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed initial demo data for Acestone Jewellery POS & Inventory System'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Beginning Acestone Jewellery database seeding...'))

        # 1. Users
        owner, _ = User.objects.get_or_create(
            email='sarah@acestone.co.ke',
            defaults={
                'name': 'Sarah Stone',
                'role': 'OWNER',
                'phone': '+254 712 345 678',
                'pin_code': '1234',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        owner.set_password('Stone@2026!')
        owner.save()

        manager, _ = User.objects.get_or_create(
            email='grace@acestone.co.ke',
            defaults={
                'name': 'Grace Mwangi',
                'role': 'MANAGER',
                'phone': '+254 720 112 233',
                'pin_code': '5678',
                'is_staff': True,
            }
        )
        manager.set_password('Grace@2026!')
        manager.save()

        emp1, _ = User.objects.get_or_create(
            email='david@acestone.co.ke',
            defaults={
                'name': 'David Kiprono',
                'role': 'EMPLOYEE',
                'phone': '+254 722 889 900',
                'commission_rate': 0.03,
            }
        )
        emp1.set_password('David@2026!')
        emp1.save()

        emp2, _ = User.objects.get_or_create(
            email='amina@acestone.co.ke',
            defaults={
                'name': 'Amina Hassan',
                'role': 'EMPLOYEE',
                'phone': '+254 733 445 566',
                'commission_rate': 0.03,
            }
        )
        emp2.set_password('Amina@2026!')
        emp2.save()

        self.stdout.write(self.style.SUCCESS('✓ Seeded 4 User Personas (Sarah, Grace, David, Amina)'))

        # 2. Showcases & Compartments
        showcase_a, _ = Showcase.objects.get_or_create(
            name='Showcase A (Fine Gold & High Jewellery)',
            defaults={'description': 'Main display counter facing entrance. 18K/22K Gold and Diamond pieces.'}
        )
        comp_a_codes = [
            ('A-01', 'Solitaire & Cocktail Rings Tray', 10),
            ('A-02', 'Diamond Tennis Bracelets Stand', 6),
            ('A-03', 'Cuban & Heavy Gold Chains Bar', 8),
            ('A-04', 'Sapphire & Emerald Pendants Rack', 8),
            ('A-05', 'Men’s Signet & Band Showcase', 12),
        ]
        for code, name, cap in comp_a_codes:
            ShelfCompartment.objects.get_or_create(
                showcase=showcase_a,
                code=code,
                defaults={'name': name, 'capacity': cap}
            )

        showcase_b, _ = Showcase.objects.get_or_create(
            name='Showcase B (Sterling Silver & Traditional Gold)',
            defaults={'description': 'Wall display cabinet. 925 Silver, Traditional Bangles and Pearls.'}
        )
        comp_b_codes = [
            ('B-01', 'Italian 925 Silver Chains Tray', 12),
            ('B-02', '22K Handcrafted Gold Bangles', 6),
            ('B-03', 'Reserved Client Orders Vault', 8),
            ('B-04', 'South Sea Pearl Drop Earrings', 10),
            ('B-05', 'New Inward Inventory Box (Empty)', 10),
        ]
        for code, name, cap in comp_b_codes:
            ShelfCompartment.objects.get_or_create(
                showcase=showcase_b,
                code=code,
                defaults={'name': name, 'capacity': cap}
            )

        self.stdout.write(self.style.SUCCESS('✓ Seeded Showcases A & B and Compartments A-01 to B-05'))

        # 3. Suppliers
        sup1, _ = Supplier.objects.get_or_create(
            name='Dubai Gold Souk Imports',
            defaults={
                'contact_person': 'Tariq Al-Mansoor',
                'phone': '+971 4 226 8899',
                'email': 'orders@dubaisouk.ae',
                'total_purchased_value': 2850000,
                'outstanding_balance': 450000,
            }
        )
        sup2, _ = Supplier.objects.get_or_create(
            name='Nairobi Precious Gems',
            defaults={
                'contact_person': 'Josephine Muthoni',
                'phone': '+254 722 100 200',
                'email': 'sales@nairobigems.co.ke',
                'total_purchased_value': 1650000,
                'outstanding_balance': 0,
            }
        )
        sup3, _ = Supplier.objects.get_or_create(
            name='Aurum Africa Refiners',
            defaults={
                'contact_person': 'Erick Otieno',
                'phone': '+254 733 900 800',
                'email': 'refinery@aurumafrica.com',
                'total_purchased_value': 980000,
                'outstanding_balance': 120000,
            }
        )

        # 4. Jewellery Inventory Items
        prod1, _ = JewelleryItem.objects.get_or_create(
            code='AC-GOLD-001',
            defaults={
                'name': '18K Yellow Gold Miami Cuban Link Chain',
                'category': 'Chains',
                'jewellery_type': 'Cuban Link Chain',
                'material': 'Gold',
                'purity': '18K (750)',
                'weight_grams': 24.5,
                'length_dimensions': '60 cm / 5mm width',
                'description': 'Classic solid 18K yellow gold Miami Cuban link chain with custom high-polish box lock and safety clasp.',
                'buying_price': 25000,
                'suggested_price': 35000,
                'min_selling_price': 29000,
                'quantity': 1,
                'showcase_id': 'Showcase A',
                'compartment_code': 'A-03',
                'supplier': sup1.name,
                'status': 'Available',
            }
        )

        prod2, _ = JewelleryItem.objects.get_or_create(
            code='AC-PND-001',
            defaults={
                'name': '18K White Gold Blue Sapphire & Diamond Royal Pendant',
                'category': 'Pendants',
                'jewellery_type': 'Gemstone Pendant',
                'material': 'Gemstone',
                'purity': '18K White Gold / 1.8ct Sapphire',
                'weight_grams': 5.1,
                'length_dimensions': '25mm x 15mm',
                'description': 'Oval faceted royal Ceylon blue sapphire surrounded by halo of diamonds.',
                'buying_price': 38000,
                'suggested_price': 55000,
                'min_selling_price': 46000,
                'quantity': 1,
                'showcase_id': 'Showcase A',
                'compartment_code': 'A-04',
                'supplier': sup2.name,
                'status': 'Available',
            }
        )

        # 5. Verified Handwritten Daily Notebook Records (Total KSh 49,450)
        notebook_entries = [
            ('Peter Philip watch', 'UNLINKED', 6000, 'Paybill', 'Partial', 'David Kiprono', 'Peter Philip', 'Watch deposit paid, balance pending collection', False),
            ('Byzantine chain', 'JEWELLERY', 20000, 'M-Pesa', 'Completed', 'David Kiprono', 'Marcus Otieno', '18K Gold Cuban link chain. Client paid via M-Pesa.', True),
            ("Men's pendant", 'JEWELLERY', 2000, 'Cash', 'Partial', 'Amina Hassan', 'Kiprotich B.', 'Deposit on Sapphire pendant', True),
            ('Earrings', 'JEWELLERY', 1800, 'M-Pesa', 'Completed', 'David Kiprono', 'Lucy Wangari', 'Pearl drop studs', True),
            ('Polish', 'SERVICE', 150, 'Cash', 'Completed', 'Amina Hassan', 'Walk-in Client', 'Deep ultrasonic polish service (0 stock deducted)', True),
            ("Men's ring", 'JEWELLERY', 4000, 'Cash', 'Completed', 'David Kiprono', 'Evans Mwiti', 'Gentleman signet onyx ring', True),
            ("Ladies' ring", 'JEWELLERY', 3500, 'Cash', 'Completed', 'Amina Hassan', 'Sharon Muthoni', 'Solitaire cocktail ring', True),
            ("Ladies' set", 'JEWELLERY', 5700, 'Cash', 'Completed', 'David Kiprono', 'Beatrice Kemboi', 'Gold-plated bridal set', True),
            ("Ladies' bracelet", 'JEWELLERY', 3500, 'Cash', 'Completed', 'Amina Hassan', 'Grace Achieng', 'Silver tennis bracelet', True),
            ("Ladies' watch", 'UNLINKED', 2800, 'M-Pesa', 'Completed', 'David Kiprono', 'Hellen Njeri', 'Rose gold mesh watch. Flagged for Boss inventory verification.', False),
        ]

        for desc, itype, amt, pmethod, pstatus, rec_by, cname, notes, rec in notebook_entries:
            NotebookDailySale.objects.get_or_create(
                item_description=desc,
                amount=amt,
                defaults={
                    'item_type': itype,
                    'payment_method': pmethod,
                    'payment_status': pstatus,
                    'recorded_by': rec_by,
                    'customer_name': cname,
                    'notes': notes,
                    'reconciled': rec,
                }
            )

        self.stdout.write(self.style.SUCCESS('✓ Seeded 10 Digitized Notebook Entries (Total: KSh 49,450)'))

        # 6. Expenses
        Expense.objects.get_or_create(
            title='Westlands Showroom Showroom Rent',
            defaults={
                'category': 'Rent',
                'amount': 180000,
                'date': timezone.now().date(),
                'description': 'Monthly prime showroom retail lease at The Mall Westlands',
                'recorded_by': 'Sarah Stone',
            }
        )
        Expense.objects.get_or_create(
            title='Armored Security & Armed Response',
            defaults={
                'category': 'Security',
                'amount': 45000,
                'date': timezone.now().date(),
                'description': '24/7 dedicated armed guards & direct alarm link to G4S Kenya',
                'recorded_by': 'Grace Mwangi',
            }
        )

        # 7. Audit Log
        AuditLog.objects.create(
            user=owner,
            action='DATABASE_INITIALIZED',
            entity_type='SYSTEM',
            entity_id='SYSTEM_BOOT',
            details='Acestone Jewellery POS database seeded with official catalog, showcases, and notebook records.',
        )

        self.stdout.write(self.style.SUCCESS('🎉 Acestone Jewellery POS database seeded successfully!'))

