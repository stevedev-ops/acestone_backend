from django.db import models

class JewelleryItem(models.Model):
    class Category(models.TextChoices):
        CHAINS = 'Chains', 'Chains'
        NECKLACES = 'Necklaces', 'Necklaces'
        RINGS = 'Rings', 'Rings'
        BRACELETS = 'Bracelets', 'Bracelets'
        BANGLES = 'Bangles', 'Bangles'
        EARRINGS = 'Earrings', 'Earrings'
        PENDANTS = 'Pendants', 'Pendants'

    class Material(models.TextChoices):
        GOLD = 'Gold', 'Gold'
        SILVER = 'Silver', 'Silver'
        PLATINUM = 'Platinum', 'Platinum'
        DIAMOND = 'Diamond', 'Diamond'
        GEMSTONE = 'Gemstone', 'Gemstone'

    class Status(models.TextChoices):
        AVAILABLE = 'Available', 'Available'
        SOLD = 'Sold', 'Sold'
        RESERVED = 'Reserved', 'Reserved'

    code = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=Category.choices)
    jewellery_type = models.CharField(max_length=100)
    material = models.CharField(max_length=50, choices=Material.choices, default=Material.GOLD)
    purity = models.CharField(max_length=50, help_text='e.g. 18K (750), 22K (916), 925 Silver')
    weight_grams = models.DecimalField(max_digits=8, decimal_places=2)
    length_dimensions = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    # Confidential pricing fields (Owner/Manager only)
    buying_price = models.DecimalField(max_digits=12, decimal_places=2, help_text='Confidential buying cost')
    suggested_price = models.DecimalField(max_digits=12, decimal_places=2, help_text='Suggested selling price')
    min_selling_price = models.DecimalField(max_digits=12, decimal_places=2, help_text='Floor minimum acceptable price')

    quantity = models.PositiveIntegerField(default=1)
    showcase_id = models.CharField(max_length=50, default='Showcase A')
    compartment_code = models.CharField(max_length=20, db_index=True, help_text='e.g. A-03')
    supplier = models.CharField(max_length=150, blank=True)
    date_purchased = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.name} ({self.compartment_code})"

class JewelleryPhoto(models.Model):
    item = models.ForeignKey(JewelleryItem, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='jewellery_photos/')
    caption = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

