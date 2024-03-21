from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('cargos', views.CargoViewSet, basename='cargos')
router.register('trucks', views.TruckViewSet, basename='trucks')

urlpatterns = [
    path('', include(router.urls))
]
