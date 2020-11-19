from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Car, Mileage_Log, Service, Part

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Car)
admin.site.register(Mileage_Log)
admin.site.register(Service)
admin.site.register(Part)