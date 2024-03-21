import random

from django.contrib import admin

from .models import Cargo, Location, Truck


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pick_up', 'delivery', 'weight', 'description')
    search_fields = ('description',)
    empty_value_display = '-empty-'
    raw_id_fields = ('pick_up', 'delivery')


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'location', 'max_weight')
    search_fields = ('number',)
    empty_value_display = '-empty-'
    raw_id_fields = ('location',)

    def save_model(self, request, obj, form, change):
        if not obj.location:
            available_locations = Location.objects.all()
            random_location = random.choice(available_locations)
            obj.location = random_location
        super().save_model(request, obj, form, change)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'state', 'zip', 'latitude', 'longitude')
    search_fields = ('city', 'state', 'zip')
    empty_value_display = '-empty-'
