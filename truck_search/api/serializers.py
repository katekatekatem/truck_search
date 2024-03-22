from geopy.distance import geodesic

from rest_framework import serializers

from trucks.models import Cargo, Truck


def cargo_truck_distances(cargo_location, condition=False):
    trucks = Truck.objects.all()
    truck_distances = []
    for truck in trucks:
        truck_location = (truck.location.latitude, truck.location.longitude)
        distance = geodesic(cargo_location, truck_location).miles
        if condition is True and distance <= 450:
            truck_distances.append(
                {'truck_number': truck.number, 'distance_miles': distance}
            )
        elif condition is False:
            truck_distances.append(
                {'truck_number': truck.number, 'distance_miles': distance}
            )
    return sorted(truck_distances, key=lambda x: x['distance_miles'])


class CargoPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cargo
        fields = '__all__'


class CargoRetriveSerializer(serializers.ModelSerializer):
    truck_distances = serializers.SerializerMethodField()

    def get_truck_distances(self, obj):
        cargo_location = (obj.pick_up.latitude, obj.pick_up.longitude)
        return cargo_truck_distances(cargo_location)

    class Meta:
        model = Cargo
        fields = '__all__'


class CargoListSerializer(serializers.ModelSerializer):
    number_of_nearby_trucks = serializers.SerializerMethodField()

    def get_number_of_nearby_trucks(self, obj):
        cargo_location = (obj.pick_up.latitude, obj.pick_up.longitude)
        truck_distances = cargo_truck_distances(cargo_location, True)

        min_distance = self.context['request'].query_params.get('min_distance')
        max_distance = self.context['request'].query_params.get('max_distance')

        if min_distance and max_distance:
            truck_distances = list(
                d for d in truck_distances if float(min_distance)
                <= d['distance_miles'] <= float(max_distance)
            )
        elif min_distance:
            truck_distances = list(
                d for d in truck_distances if d['distance_miles']
                >= float(min_distance)
            )
        elif max_distance:
            truck_distances = list(
                d for d in truck_distances if d['distance_miles']
                <= float(max_distance)
            )
        return len(truck_distances)

    class Meta:
        model = Cargo
        fields = ['pick_up', 'delivery', 'number_of_nearby_trucks']


class CargoUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cargo
        fields = '__all__'
        read_only_fields = ['pick_up', 'delivery']


class TruckSerializer(serializers.ModelSerializer):

    class Meta:
        model = Truck
        fields = '__all__'
