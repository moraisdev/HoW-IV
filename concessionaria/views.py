from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from concessionaria.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'car_dealer/login.html')
    else:
        return render(request, 'car_dealer/home_page.html')

def login(request):
    return render(request, 'car_dealer/login.html')


def auth_view(request):
    if request.user.is_authenticated:
        return render(request, 'car_dealer/home_page.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            car_dealer = CarDealer.objects.get(car_dealer = user)
        except:
            car_dealer = None
        if car_dealer is not None:
            auth.login(request, user)
            return render(request, 'car_dealer/home_page.html')
        else:
            return render(request, 'car_dealer/login_failed.html')

def logout_view(request):
    auth.logout(request)
    return render(request, 'car_dealer/login.html')

def register(request):
    return render(request, 'car_dealer/register.html')

def registration(request):
    username = request.POST['username']
    password = request.POST['password']
    mobile = request.POST['mobile']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    city = request.POST['city']
    city = city.lower()
    pincode = request.POST['pincode']

    try:
        user = User.objects.create_user(username = username, password = password, email = email)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
    except:
        return render(request, 'car_dealer/registration_error.html')
    try:
        area = Area.objects.get(city = city, pincode = pincode)
    except:
        area = None
    if area is not None:
        car_dealer = CarDealer(car_dealer = user, mobile = mobile, area=area)
    else:
        area = Area(city = city, pincode = pincode)
        area.save()
        area = Area.objects.get(city = city, pincode = pincode)
        car_dealer = CarDealer(car_dealer = user, mobile = mobile, area=area)
    car_dealer.save()
    return render(request, 'car_dealer/registered.html')

@login_required
def add_vehicle(request):
    car_name = request.POST['car_name']
    color = request.POST['color']
    cd = CarDealer.objects.get(car_dealer=request.user)
    city = request.POST['city']
    city = city.lower()
    pincode = request.POST['pincode']
    description = request.POST['description']
    capacity = request.POST['capacity']
    try:
        area = Area.objects.get(city = city, pincode = pincode)
    except:
        area = None
    if area is not None:
        car = Vehicles(car_name=car_name, color=color, dealer=cd, area = area, description = description, capacity=capacity)
    else:
        area = Area(city = city, pincode = pincode)
        area.save()
        area = Area.objects.get(city = city, pincode = pincode)
        car = Vehicles(car_name=car_name, color=color, dealer=cd, area = area,description=description, capacity=capacity)
    car.save()
    return render(request, 'car_dealer/vehicle_added.html')

@login_required
def manage_vehicles(request):
    username = request.user
    user = User.objects.get(username = username)
    car_dealer = CarDealer.objects.get(car_dealer = user)
    vehicle_list = []
    vehicles = Vehicles.objects.filter(dealer = car_dealer)
    for v in vehicles:
        vehicle_list.append(v)
    return render(request, 'car_dealer/manage.html', {'vehicle_list':vehicle_list})

@login_required
def delete(request):
    veh_id = request.POST['id']
    vehicle = Vehicles.objects.get(id = veh_id)
    vehicle.delete()
    return HttpResponseRedirect('/concessionaria/manage_vehicles/')
