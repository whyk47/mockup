from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point
from django.db.models.manager import BaseManager
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Q

from .location_service_exceptions import NoAddressException


class LocationService:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(LocationService, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="location_service")

    def geocode(self, address: str) -> tuple[float, float]:
        location = self.geolocator.geocode(address)
        if not location:
            raise Exception("Location not found")
        return location.latitude, location.longitude
    
    def get_point(self, address: str) -> Point:
        lat, lng = self.geocode(address)
        return Point(lng, lat, srid=4326)
    
    def dist_filter(self, queryset: BaseManager, address: str, dist_km: int = 20) -> BaseManager:
        user_location = self.get_point(address)
        queryset = queryset.annotate(distance=Distance('location', user_location)).filter(
            Q(distance__lte=dist_km * 1000) |
            Q(remote=True)
            )
        return queryset
    
    def dist_sort(self, queryset: BaseManager, address: str) -> BaseManager:
        if not address:
            raise NoAddressException("Address is required")
        user_location = self.get_point(address)
        queryset = queryset.annotate(distance=Distance('location', user_location))
        return queryset.order_by('-remote', 'distance')