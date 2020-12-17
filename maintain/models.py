from django.db import models
from django.db.models import Q, F
from django.contrib.auth.models import AbstractUser
from datetime import datetime, date, timedelta

# Create your models here.

class User(AbstractUser):

    @property
    def default_car(self):
        try:
            car = self.cars.get(default=True)
        except Car.DoesNotExist:
            car = None
        return car

class Car(models.Model):
    vin = models.CharField(max_length=17)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    purchase_date = models.DateField(blank=True, null=True)
    purchase_mileage = models.CharField(max_length=6, blank=True, null=True)
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="cars")
    default = models.BooleanField(default=False)

    # Get current mileage from mileage log (returns int)
    @property
    def current_mileage(self):
        log = self.logs.order_by(F('mileage').desc())
        return log.first().mileage

    # Get starting mileage from mileage log (returns int)
    @property
    def starting_mileage(self):
        log = self.logs.order_by('mileage')
        return log.first().mileage

    # Return all logs (ascending)
    @property
    def get_logs(self):
        return self.logs.all().order_by('timestamp')

    # Return all logs in descending order that had service performed
    @property
    def get_service_logs(self):
        return self.logs.filter(services__name__isnull=False).order_by(F('timestamp').desc())

    # Return all logs that had fuel logged
    @property
    def get_fuel_logs(self):
        return self.logs.filter(fuel__amount__isnull=False).order_by('timestamp')

    # Return all upcoming reminders
    @property
    def get_reminders_upcoming(self):
        upcoming_time_delta = timedelta(days=30)
        upcoming_mileage_delta = 1000
        return (Reminder.objects.filter(service__log__car = self).filter(completed = False)
        .filter(Q(date__gte = date.today()) | Q(date__isnull = True))
        .filter(Q(mileage__gte = self.current_mileage) | Q(mileage__isnull = True))
        .filter(Q(date__lte = date.today() + upcoming_time_delta) | 
        Q(mileage__lte = self.current_mileage + upcoming_mileage_delta)))

    # Return all past due reminders
    @property
    def get_reminders_overdue(self):
        return (Reminder.objects.filter(service__log__car = self).filter(completed = False)
        .filter(Q(date__lte = date.today() - timedelta(days=1)) | 
        Q(mileage__lte = self.current_mileage - 1)))

    @property
    def info(self):
        return f"{self.year} {self.make} {self.model}, {self.current_mileage} miles"

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

    def serialize(self):
        return {
            "vin": self.vin,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "current mileage": self.current_mileage,
            "purchase date": self.purchase_date,
        }
    
class Mileage_Log(models.Model):
    timestamp = models.DateField(default=date.today())
    mileage = models.PositiveIntegerField()
    car = models.ForeignKey("Car", on_delete=models.CASCADE, related_name="logs")

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

    # Return the time delta between service and reminder dates
    def duration(self):
        log_date = self.service.log.timestamp
        duration = self.date - log_date
        return int(round((duration.days/365) * 12))

    # Return the mileage delta between service and reminder
    def mile_amount(self):
        log_mileage = self.service.log.mileage
        mile_amount = self.mileage - log_mileage
        return mile_amount

    def serialize(self):
        return {
            "reminder": {
                "id": self.id,
                "duration": self.duration(),
                "mile-amount": self.mile_amount(),
            },
            "service": {
                "name": self.service.name,
                "parts": [{"name": part.name, "number": part.number} for part in self.service.parts.all()]
            }
        }
