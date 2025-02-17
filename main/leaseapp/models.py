from django.db import models
from django.contrib.auth.models import User

class VehicleType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name


class EngineType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    class Edition(models.TextChoices):
        LIMITED_EDITION = "LE", "Limited Edition"
        SPORT_EDITION = "SE", "Sport Edition"
        EXCLUSIVE_LIMITED_EDITION = "XLE", "Exclusive Limited Edition"
    id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=55)
    model = models.CharField(max_length=55)
    year = models.CharField(max_length=4)
    color = models.CharField(max_length=55)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    engine_type = models.ForeignKey(EngineType, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Car_Profile")
    plate_number = models.CharField(max_length=10)
    available = models.BooleanField(default=True)
    millage = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"

class LeasePrice(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    daily_price = models.DecimalField(max_digits=12, decimal_places=2)
    weekly_price = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_price = models.DecimalField(max_digits=12, decimal_places=2)

    # def __str__(self):
    #     return self.vehicle


from django.core.exceptions import ValidationError


class Lease(models.Model):
    class DurationType(models.TextChoices):
        DAY = "Day", "Day"
        WEEK = "Week", "Week"
        MONTH = "Month", "Month"

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration_type = models.CharField(max_length=10, choices=DurationType.choices, default=DurationType.DAY)
    vehicle = models.ForeignKey("Vehicle", on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    user_ip = models.GenericIPAddressField()
    profile_image = models.ImageField(upload_to="Client_photo")
    phone_number_1 = models.CharField(max_length=15)
    phone_number_2 = models.CharField(max_length=15, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration = models.PositiveIntegerField(null=True, blank=True)
    aggreement = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        try:
            lease_price = LeasePrice.objects.get(vechicle=self.vechicle)
        except LeasePrice.DoesNotExist:
            raise ValidationError("No lease price set for this vehicle.")

        if self.duration_type == self.DurationType.DAY:
            price_per_unit = lease_price.daily_price
        elif self.duration_type == self.DurationType.WEEK:
            price_per_unit = lease_price.weekly_price
        elif self.duration_type == self.DurationType.MONTH:
            price_per_unit = lease_price.monthly_price
        else:
            raise ValidationError("Invalid duration type.")
        if not self.duration:
            raise ValidationError("Duration must be provided.")
        self.cost = price_per_unit * self.duration
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
