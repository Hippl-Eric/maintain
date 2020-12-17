import csv
import json
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import F, Q
from datetime import datetime, date, timedelta

from .models import User, Car, Mileage_Log, Fuel, Service, Part, Reminder

# Create your views here.

@login_required(login_url='login')
def index(request):

    # Add new car
    if request.method == "POST":

        # Parse new car form data
        make = request.POST["make"]
        model = request.POST["model"]
        year = request.POST["year"]
        vin = request.POST["vin"]
        starting_mile = request.POST["starting-mile"]
        purchase = request.POST["purchase-date"]
        month, day, year = int(purchase[0:2]), int(purchase[3:5]), int(purchase[6:10])
        purchase_date = date(year=year, month=month, day=day)

        # Create new car and add to session
        car = Car(vin=vin, make=make, model=model, year=year, purchase_date=purchase_date, purchase_mileage=starting_mile, owner=request.user)
        car.save()

        # Create first mileage log
        current_mile = request.POST["current-mile"]
        log = Mileage_Log(mileage=current_mile, timestamp=date.today(), car=car)
        log.save()

        # Set new car as default
        update_default_car(request=request, car=car)

        return redirect(reverse("index"))

    # Return index page and all cars
    else:

        # Get all cars owned by user
        cars = request.user.cars.all()
        return render(request, "maintain/index.html", {
            "cars": cars,
        })

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse(index))
        else:
            return render(request, "maintain/login.html", {
                "alert": "warning",
                "alert_message": "Invalid username or password"
            })
    else:
        return render(request, "maintain/login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "maintain/register.html", {
                "alert": "warning",
                "alert_message": "Passwords must match"
            })

        # Create new user
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError:
            return render(request, "maintain/register.html", {
                "alert": "warning",
                "alert_message": "Username not available"
            })
        login(request, user)
        return redirect(reverse("index"))
    else:
        return render(request, "maintain/register.html")

def logout_view(request):
    logout(request)
    return redirect(reverse(index))

@login_required(login_url='login')
def car_mileage_view(request):

    # Get car from session
    car = get_default_car(request)
    if not car:
        return redirect(reverse("index"))

    # Mileage log form submission
    if request.method == "POST":
        
        # Parse form data
        mileage = request.POST["mileage"]
        fuel = request.POST["fuel"]
        fuel = round(float(fuel), 2)
        log_date = request.POST["date"]
        month, day, year = int(log_date[0:2]), int(log_date[3:5]), int(log_date[6:10])
        log_date = date(year=year, month=month, day=day)

        # Create new mileage/fuel log
        log = Mileage_Log(timestamp=log_date, mileage=mileage, car=car)
        log.save()
        fuel = Fuel(amount=fuel, log=log)
        fuel.save()

        return redirect(reverse('car_mileage'))

    # Return mileage page
    else:
        
        # Get overdue reminders (for alert)
        overdue_reminders = car.get_reminders_overdue
        return render(request, "maintain/car_mileage.html", {
            "car": car,
            "overdue_reminders": overdue_reminders,
        })

@login_required(login_url='login')
def car_service_view(request):

    # Get car from session
    car = get_default_car(request)
    if not car:
        return redirect(reverse("index"))
    
    # New submission from service form
    if request.method == "POST":

        # Ensure minimum form data received
        if not request.POST["date"] or not request.POST["mileage"] or not request.POST["service"]:
            return redirect(reverse("car_service"))

        # Parse date (MM/DD/YYYY)
        form_date = request.POST["date"]
        month, day, year = int(form_date[0:2]), int(form_date[3:5]), int(form_date[6:10])
        log_date = date(year=year, month=month, day=day)

        # Parse mileage (positive integer)
        mileage = int(request.POST["mileage"])
        mile_log = Mileage_Log(timestamp=log_date, mileage=mileage, car=car)
        mile_log.save()

        # Create service
        service_name = request.POST["service"]
        service = Service(name=service_name, log=mile_log)
        service.save()

        # Get or create parts
        form_parts = {key: val for key, val in request.POST.items() if key.startswith("part")}
        num_parts = len(form_parts)//2
        for i in range(num_parts):
            part_name = form_parts[f'part-name-{i+1}']
            if part_name:
                part_number = form_parts[f'part-number-{i+1}']
                part, created = Part.objects.get_or_create(name=part_name, number=part_number)
                part.services.add(service)

        # Create reminder
        if request.POST["duration"] or request.POST["mile-amount"]:
            reminder = Reminder(service=service)
            if request.POST["duration"]:
                duration = int(365 * (int(request.POST["duration"]) / 12))
                reminder_date = log_date + timedelta(days=duration)
                reminder.date = reminder_date
            if request.POST["mile-amount"]:
                mile_amount = int(request.POST["mile-amount"])
                reminder_mile = mileage + mile_amount
                reminder.mileage = reminder_mile
            reminder.save()

        # Update previous reminder complete
        if request.POST["reminder-id"]:
            rem_id = request.POST["reminder-id"]
            try:
                past_rem = Reminder.objects.get(id=rem_id, service__log__car=car)
                past_rem.completed = True
                past_rem.save()
            except Reminder.DoesNotExist:
                pass

        return redirect(reverse("car_service"))

    # Return service page
    else:

        # Get past service logs
        past_service_logs = car.get_service_logs

        # Get upcoming and overdue reminders
        upcoming_reminders = car.get_reminders_upcoming
        overdue_reminders = car.get_reminders_overdue

        # Return car service page
        return render(request, "maintain/car_service.html", {
            "past_service_logs": past_service_logs,
            "upcoming_reminders": upcoming_reminders,
            "overdue_reminders": overdue_reminders,
        })

def set_default_car(request, car_id):
    """ JS: Set the default car clicked by user """
    try:
        car = request.user.cars.get(pk=car_id)
    except:
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Set or update default car
    update_default_car(request, car)
    return HttpResponse(status=200)

def update_default_car(request, car):
    """ Helper: Set/update car in the database and request session """
    
    # Check database for previous default car and clear
    def_car = request.user.default_car
    if def_car:
        def_car.default = False
        def_car.save()
    
    # Set car as default
    car.default = True
    car.save()

    # Store in session
    request.session['default_car'] = car.id

def get_default_car(request):
    """ Helper: Return car object from id stored in session """
    try:
        car_id = request.session.get("default_car")
        car = request.user.cars.get(pk=car_id)
        return car
    except Car.DoesNotExist:
        return None

def mileage_logs(request):
    """ JS: Return mileage log data used for plotting """
    if request.method == "PUT":

        # Load request data
        data = json.loads(request.body)

        # Determine whether default car or all cars
        if data.get("car") == "default":
            cars = [get_default_car(request)]
        if data.get("car") == "all":
            cars = request.user.cars.all()

        # Plot total mileage
        if data.get("type") == "miles":
            data = []
            for car in cars:
                logs = car.get_logs
                obj = {
                    "label": f"{car.make} {car.model}",
                    "data": [{"x": str(log.timestamp), "y": log.mileage} for log in logs]
                    }
                data.append(obj)
            return JsonResponse(json.dumps(data), safe=False)

    # PUT method required
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

def service_data(request):
    """ JS: Return reminder data to pre-fill service form """
    if request.method == "PUT":

        # Load request data and grab reminder id
        data = json.loads(request.body)
        rem_id = data.get("rem_id")

        # Ensure valid reminder
        try:
            car = get_default_car(request)
            reminder = Reminder.objects.get(service__log__car=car, id=rem_id)
        except Reminder.DoesNotExist:
            return JsonResponse({"error": "Invalid request"}, status=400)
        
        # Serialize reminder and return data
        reminder_data = reminder.serialize()
        return JsonResponse(json.dumps(reminder_data), safe=False)

    # PUT method required
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

def csv_data(request):
    """ Return csv file object for default car's past services """

    # Get car from session
    car = get_default_car(request)

    # Get past service logs
    past_service_logs = car.get_service_logs

    # Parse to csv rows
    header_row = ["Vehicle", "Date", "Mileage", "Service Name", "Parts"]
    csv_rows = []
    for log in past_service_logs:
        row =[log.car, log.timestamp, log.mileage]
        service = log.services.get()
        row.append(service.name)
        parts = ""
        for part in service.parts.all():
            p = f"({part.name}, {part.number}) "
            parts += p
        row.append(parts)
        csv_rows.append(row)

    # https://docs.djangoproject.com/en/3.1/howto/outputting-csv/#using-the-python-csv-library
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="service_log.csv"'
    writer = csv.writer(response)
    writer.writerow(header_row)
    writer.writerows(csv_rows)
    return response
