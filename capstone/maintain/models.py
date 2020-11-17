from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Car(models.Model):
    vin = models.CharField(max_length=17, blank=False)
    make = models.CharField(max_length=50, blank=False)
    model = models.CharField(max_length=50, blank=False)
    year = models.CharField(max_length=4, blank=False)
    purchase_date = models.DateField()
    mileage = models.CharField(max_length=6)
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="cars")
    default = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "vin": self.vin,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "purchase_date": self.purchase_date,
            "mileage": self.mileage,
            "owner": self.owner.username,
            "default": self.default
        }
