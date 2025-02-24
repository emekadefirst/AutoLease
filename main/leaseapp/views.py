from django.shortcuts import render, get_object_or_404, redirect
from .models import Vehicle, EngineType, VehicleType
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login

# Create your views here.
def main(request):
    return render(request, 'landing.html')


def base(request):
    return render(request, 'base.html')


def detail(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    return render(request, 'detail.html', {"vehicle": vehicle})

def home(request):
    vehicles = Vehicle.objects.all()
    engintype = EngineType.objects.all()
    vehicletype = VehicleType.objects.all()
    return render(request, 'index.html', {"vehicles": vehicles, "engintype": engintype, "vehicletype": vehicletype})


from django.shortcuts import render
from .models import Vehicle, EngineType, VehicleType  # Import missing models


def vehicle_filter(request):
    etype = request.GET.get("etype")
    vtype = request.GET.get("type")

    vehicles = Vehicle.objects.all()

    if etype:
        vehicles = vehicles.filter(engine_type__name=etype)  
    if vtype:
        vehicles = vehicles.filter(vehicle_type__name=vtype)
    engintype = EngineType.objects.all()
    vehicletype = VehicleType.objects.all()

    return render(
        request,
        "index.html",
        {"vehicles": vehicles, "engintype": engintype, "vehicletype": vehicletype},
    )

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("Home page")
        else:
            return redirect("login")
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            user = User.objects.create(username=username, email=email)
            user.set_password(password1)
            user.save()
            auth_login(request, user)
            return redirect("/home")
    return render(request, 'signup.html')


def logout_user(request):
    logout(request)
    return redirect("/login")
