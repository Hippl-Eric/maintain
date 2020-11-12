from django.shortcuts import render
from django.http import HttpResponse
from maintain.helpers import call_car_md, get_credits

# Create your views here.

def index(request):
    return HttpResponse("Hey, the maintain app")