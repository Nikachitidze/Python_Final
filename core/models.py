from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    favorite_cars = models.ManyToManyField('Car', related_name='favorited_by', blank=True)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)



    def __str__(self):
        return f"{self.username} ({self.phone_number})"

class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('auto', 'ავტომატიკა'),
        ('manual', 'მექანიკა'),
        ('tiptronic', 'ტიპტრონიკი'),
    ]

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    fuel_capacity = models.PositiveIntegerField()
    photo1 = models.ImageField(upload_to='cars/')
    photo2 = models.ImageField(upload_to='cars/')
    photo3 = models.ImageField(upload_to='cars/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"



class Rent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey('Car', on_delete=models.CASCADE, related_name='rents')
    rent_start_date = models.DateField()
    rent_end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} rented {self.car.brand} {self.car.model} ({self.rent_start_date} - {self.rent_end_date})"




class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.phone_number} - {self.message[:30]}"

