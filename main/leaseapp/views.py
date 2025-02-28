from django.shortcuts import render, get_object_or_404, redirect
from .models import Vehicle, EngineType, VehicleType, LeasePrice
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from .paystack import make_payment
from django.shortcuts import render
from .models import Vehicle, EngineType, VehicleType  # Import missing models

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Lease, Vehicle
import json


# Create your views here.
def main(request):
    vehicles = Vehicle.objects.all()[:3]
    return render(request, 'landing.html', {"vehicles": vehicles})


def base(request):
    return render(request, 'base.html')


def detail(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    lease = get_object_or_404(LeasePrice, vehicle=vehicle)
    return render(request, 'detail.html', {"vehicle": vehicle, "lease": lease})

def home(request):
    vehicles = Vehicle.objects.all()
    engintype = EngineType.objects.all()
    vehicletype = VehicleType.objects.all()
    return render(request, 'index.html', {"vehicles": vehicles, "engintype": engintype, "vehicletype": vehicletype})


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


@method_decorator(csrf_exempt, name="dispatch")  # Disable CSRF for testing (use proper auth in production)
@login_required
def lease(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  
            user_ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR"))
            if user_ip:
                user_ip = user_ip.split(",")[0]

            user = request.user
            duration = data.get("duration")
            vehicle_id = data.get("vehicle")
            duration_type = data.get("duration_type")
            profile_image = request.FILES.get("profile_image")  # For file uploads
            phone_number_1 = data.get("phone_number_1")
            phone_number_2 = data.get("phone_number_2")
            start_date = data.get("start_date")
            end_date = data.get("end_date")
            try:
                vehicle = Vehicle.objects.get(id=vehicle_id)
            except Vehicle.DoesNotExist:
                return JsonResponse({"error": "Vehicle not found"}, status=404)
            lease = Lease.objects.create(
                user=user,
                vehicle=vehicle,
                duration=duration,
                duration_type=duration_type,
                profile_image=profile_image,
                phone_number_1=phone_number_1,
                phone_number_2=phone_number_2,
                start_date=start_date,
                end_date=end_date,
                user_ip=user_ip,
            )
            return JsonResponse(
                {
                    "message": "Lease created successfully",
                    "lease_id": lease.id,
                    "user": lease.user.username,
                    "vehicle": lease.vehicle.id,
                    "start_date": lease.start_date,
                    "end_date": lease.end_date,
                },
                status=201,
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


def logout_user(request):
    logout(request)
    return redirect("/login")
