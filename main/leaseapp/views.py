from django.shortcuts import render, get_object_or_404, redirect
from .models import Vehicle, EngineType, VehicleType

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


def vehicle_filter(request):
    etype = request.GET.get('etype')
    type = request.GET.get('type')
    year = request.GET.get('year')
    brand = request.GET.get('brand')
    filters = {}
    if etype:
        filters["engine_type"] = etype
    if type:
        filters["typevehicle_type"] = type
    if year:
        filters["year"] = year
    if brand:
        filters["brand"] = year
    vehicles = Vehicle.objects.filter(**filters)
    return render(request, 'index.html', {'vehicle': vehicles})
