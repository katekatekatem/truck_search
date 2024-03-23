import random

from truck_search.celery import app


@app.task()
def update_locations():
    from trucks.models import Location, Truck
    trucks = Truck.objects.all()
    for truck in trucks:
        available_locations = Location.objects.exclude(id=truck.location.id)
        random_location = random.choice(available_locations)
        truck.location = random_location
        truck.save()
