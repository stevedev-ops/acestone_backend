from django.db import models

class Showcase(models.Model):
    name = models.CharField(max_length=100) # e.g. "Showcase A (Fine Gold)"
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ShelfCompartment(models.Model):
    showcase = models.ForeignKey(Showcase, related_name='compartments', on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True, db_index=True) # e.g. "A-01", "A-03"
    name = models.CharField(max_length=150)
    capacity = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"{self.code} ({self.name})"

