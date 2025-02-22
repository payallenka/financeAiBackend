import uuid
from django.db import models

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    user_id = models.CharField(max_length=255)  # Store Firebase UID
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    category = models.CharField(
        max_length=20,
        choices=[
            ('food', 'Food'),
            ('transport', 'Transport'),
            ('shopping', 'Shopping'),
            ('bills', 'Bills'),
            ('other', 'Other'),
        ],
        default='other'
    )

    def __str__(self):
        return f"{self.description} - {self.amount}"
