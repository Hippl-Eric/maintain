from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("defaultcar/<int:car_id>", views.set_default_car, name="defaultcar"),
    path("car/info", views.car_info_view, name="car_info"),
    path("car/mileage", views.car_mileage_view, name="car_mileage"),
    path("car/service", views.car_service_view, name="car_service"),
    path("plotlogs", views.mileage_logs, name="plotlogs"),
]