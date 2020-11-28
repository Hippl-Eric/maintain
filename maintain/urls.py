from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("car/<int:car_id>", views.get_car, name="car"),
    path("car/info", views.car_info_view, name="car_info"),
    path("car/mileage", views.car_mileage_view, name="car_mileage"),
    path("car/service", views.car_service_view, name="car_service"),
]