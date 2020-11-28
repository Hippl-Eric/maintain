import datetime
import random
from .models import *

def save_data():

    # Get all cars
    user = User.objects.get(username="ehippler")
    cars = user.cars.all()

    for car in cars:
        make = car.make
        M = make[0]

        # Create 10 mileage logs with fuel
        if M == "H":
            mileage = 10000
            mil_int = 400
            date = datetime.datetime(2020, 1, 15)
        else:
            mileage = 2300
            mil_int = 270
            date = datetime.datetime(2020, 1, 3)

        for _ in range(10):
            mile_log = Mileage_Log(timestamp=date, mileage=mileage, car=car)
            mile_log.save()

            fuel_amount = round(random.randrange(11, 17) + random.random(), 2)
            fuel = Fuel(amount=fuel_amount, log=mile_log)
            fuel.save()

            mileage += mil_int
            date += datetime.timedelta(days=25)


        # Create 3 logs for services

        # Create 3 services

        # Create 3 Parts

        # Create 3 reminders