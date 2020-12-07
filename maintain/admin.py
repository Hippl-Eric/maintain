from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Car, Mileage_Log, Fuel, Service, Part, Reminder

class CarAdmin(admin.ModelAdmin):
    list_display = ["owner", "id", "make", "model"]

class LogAdmin(admin.ModelAdmin):
    list_display = ["timestamp", "car", "mileage"]

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Mileage_Log, LogAdmin)
admin.site.register(Fuel)
admin.site.register(Service)
admin.site.register(Part)
admin.site.register(Reminder)