from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from django.core.exceptions import ValidationError

from users.models import CustomUser


class Product(models.Model):
    is_cleaned = False

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    image = models.ImageField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'Product<{self.name}, {self.owner}>'

    def get_image_url(self):
        return self.image.url

    def get_order_count(self):
        return self.order_set.count()

    def full_clean(self, *args, **kwargs):
        super().full_clean(*args, **kwargs)
        if not self.owner.is_nursery_manager():
            raise ValidationError('Product owner must be a nursery manager')

        # we don't want to run a clean more than once
        self.is_cleaned = True

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super().save(*args, **kwargs)


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Canceled', 'Canceled'),
        ('Delivered', 'Delivered'),
    )
    buyer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='orders_placed')
    seller = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='orders_received')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, choices=STATUS, default='Pending')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
