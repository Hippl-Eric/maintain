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

    # GET index page
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

    if request.method == "POST":
        pass
        # TODO log mileage/fuel log

    else:

        # Get car from session
        car = get_default_car(request)
        
        # Get overdue reminders
        overdue_reminders = car.get_reminders_overdue

        # Return car mileage page
        return render(request, "maintain/car_mileage.html", {
            "car": car,
            "overdue_reminders": overdue_reminders,
        })

@login_required(login_url='login')
def car_service_view(request):

    # Get car from session
    car = get_default_car(request)
        
    if request.method == "POST":
        post_dict = request.POST

        # Parse date (MM/DD/YYYY)
        form_date = request.POST["date"]
        month, day, year = int(form_date[0:2]), int(form_date[3:5]), int(form_date[6:10])
        log_date = date(year=year, month=month, day=day)

        # Parse mileage (positive integer)
        mileage = int(request.POST["mileage"])

        log = Log_Obj(date=log_date, mileage=mileage)
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
            part_number = form_parts[f'part-number-{i+1}']
            part, created = Part.objects.get_or_create(name=part_name, number=part_number)
            part.services.add(service)

        # TODO Create reminder

        return redirect(reverse("car_service"))

    else:

        # Get past service logs
        past_service_logs = car.get_service_logs

        # Get upcoming reminders
        upcoming_reminders = car.get_reminders_upcoming

        # Get overdue reminders
        overdue_reminders = car.get_reminders_overdue

        # Return car service page
        return render(request, "maintain/car_service.html", {
            "past_service_logs": past_service_logs,
            "upcoming_reminders": upcoming_reminders,
            "overdue_reminders": overdue_reminders,
        })

@login_required(login_url='login')
def set_default_car(request, car_id):
    try:
        car = request.user.cars.get(pk=car_id)
    except:
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Set or update default car
    update_default_car(request, car)
    return HttpResponse(status=200)

def update_default_car(request, car):
    """ Set/update car in the request session """
    request.session['default_car'] = car.id
    request.session['default_car_info'] = f"{car.year} {car.make} {car.model}, {car.current_mileage} miles"

def get_default_car(request):
    """ Return car object from id stored in session """
    try:
        car_id = request.session.get("default_car")
        car = request.user.cars.get(pk=car_id)
        return car
    except Car.DoesNotExist:
        return None

def mileage_logs(request):
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

        # Plot MPG
        if data.get("type") == "mpg":
            pass
            # TODO

    # PUT method required
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

