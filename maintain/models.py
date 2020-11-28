from django.db import models
from django.db.models import Q, F
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Car(models.Model):
    vin = models.CharField(max_length=17)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    purchase_date = models.DateField(blank=True, null=True)
    starting_mileage = models.CharField(max_length=6, blank=True, null=True)
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="cars")
    default = models.BooleanField(default=False)


    # TODO Constraint default must be unique
    class Meta:
        models.constraints = [
            models.UniqueConstraint(fields=['owner', 'default'], name='one_default_car')
        ]

    # Use property to get current mileage from mileage log (returns int)
    @property
    def current_mileage(self):
        log = self.logs.order_by(F('mileage').desc())
        return log.first().mileage

    def __str__(self):
        return f"{self.make} {self.model}"

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
    
    def session_store(self):
        return {
            "id": self.id,
            "name": f"{self.make} {self.model}"
        }

class Mileage_LogManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by(F('timestamp').desc())

class Mileage_Log(models.Model):
    timestamp = models.DateTimeField(auto_created=True)
    mileage = models.PositiveIntegerField()
    car = models.ForeignKey("Car", on_delete=models.CASCADE, related_name="logs")
    objects = Mileage_LogManager

    def __str__(self):
        return f"{self.mileage}, {self.car}"

class Fuel(models.Model):
    amount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    log = models.OneToOneField("Mileage_Log", on_delete=models.CASCADE, related_name="fuel")

    def __str__(self):
        return f"{self.amount}, {self.log}"

class Service(models.Model):
    name = models.CharField(max_length=50)
    log = models.ForeignKey("Mileage_Log", on_delete=models.CASCADE, related_name="services")

    def __str__(self):
        return f"{self.name}, {self.log}"

class Part(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50, blank=True, null=True)
    services = models.ManyToManyField("Service", related_name="parts")

    def __str__(self):
        return f"{self.name}"

class Reminder(models.Model):
    date = models.DateField(blank=True, null=True)
    mileage = models.PositiveIntegerField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    service = models.OneToOneField("Service", on_delete=models.CASCADE, related_name="reminder")

    def __str__(self):
        return f"{self.service}, {self.date}, {self.mileage}, {self.completed}"
