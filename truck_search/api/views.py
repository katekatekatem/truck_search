from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from . import serializers
from .filters import CargoFilter
from trucks.models import Cargo, Truck


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend]
    filterset_class = CargoFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CargoPostSerializer
        if self.request.method == 'PATCH':
            return serializers.CargoUpdateSerializer
        if self.action == 'retrieve':
            return serializers.CargoRetriveSerializer
        if self.action == 'list':
            return serializers.CargoListSerializer


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = serializers.TruckSerializer
    http_method_names = ['patch']
