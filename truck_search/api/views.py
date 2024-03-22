from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response

from . import serializers
from trucks.models import Cargo, Truck


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CargoPostSerializer
        if self.request.method == 'PATCH':
            return serializers.CargoUpdateSerializer
        if self.action == 'retrieve':
            return serializers.CargoRetriveSerializer
        if self.action == 'list':
            return serializers.CargoListSerializer

    def list(self, request, *args, **kwargs):
        min_weight = request.query_params.get('min_weight')
        max_weight = request.query_params.get('max_weight')
        if min_weight and max_weight:
            queryset = Cargo.objects.filter(
                weight__gt=min_weight,
                weight__lt=max_weight
            )
        elif min_weight:
            queryset = Cargo.objects.filter(weight__gt=min_weight)
        elif max_weight:
            queryset = Cargo.objects.filter(weight__lt=max_weight)
        else:
            queryset = Cargo.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = serializers.TruckSerializer
    http_method_names = ['patch']
