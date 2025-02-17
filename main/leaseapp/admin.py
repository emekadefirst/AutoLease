from django.contrib import admin
from .models import Vehicle, VehicleType, LeasePrice, Lease, EngineType

class VehicleAdmin(admin.ModelAdmin):
    list_display = ['id', 'model', 'brand', 'year', 'color']

class EngineTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class LeasePriceAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicle', 'daily_price', 'weekly_price', 'monthly_price']


class LeaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicle', 'duration', 'cost', 'created_at']


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleType, VehicleTypeAdmin)
admin.site.register(LeasePrice, LeasePriceAdmin)
admin.site.register(Lease, LeaseAdmin)
admin.site.register(EngineType, EngineTypeAdmin)