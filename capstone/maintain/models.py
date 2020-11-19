from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Car(models.Model):
    vin = models.CharField(max_length=17)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    purchase_date = models.DateField(blank=True)
    starting_mileage = models.CharField(max_length=6, blank=True)
    # current_mileage = models.CharField(max_length=6)
    # Use property to get to most current mileage from mileage log
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="cars")
    default = models.BooleanField(default=False)

    # TODO Constraint default must be unique

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

class Mileage_Log(models.Model):
    timestamp = models.DateTimeField(auto_created=True)
    mileage = models.PositiveIntegerField()
    gas_amount = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    car = models.ForeignKey("Car", on_delete=models.CASCADE, related_name="logs")

class Service(models.Model):
    name = models.CharField(max_length=50)
    logs = models.ManyToManyField("Mileage_Log", related_name="services")

class Part(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50, blank=True)
    logs = models.ManyToManyField("Mileage_Log", blank=True, related_name="parts")
    services = models.ManyToManyField("Service", blank=True, related_name="parts")
    # Add constraint that both logs and services cannot be blank
    # Add constraint that if log is provided, service is blank, and vice versa 
