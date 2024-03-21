import asyncio
import random
import threading
import time

from .models import Truck, Location


def update_locations():
    while True:
        trucks = Truck.objects.all()
        for truck in trucks:
            available_locations = Location.objects.all()
            random_location = random.choice(available_locations)
            truck.location = random_location
            truck.save()
        time.sleep(180)

update_thread = threading.Thread(target=update_locations)
update_thread.start()
