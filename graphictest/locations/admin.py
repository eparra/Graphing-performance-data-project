кfrom django.contrib import admin
from locations.models import Location, Measurement


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    pass
