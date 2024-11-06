import requests
import os
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.db.models.manager import BaseManager
from .exceptions import GOOGLE_MAPS_REQUEST_ERROR

def geocode_address(address: str) -> tuple[float, float]:
    api_key = os.environ.get('GOOGLE_MAP_API_KEY')
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    response = requests.get(url)
    print(response.json())
    location = response.json()['results'][0]['geometry']['location']
    return location['lat'], location['lng']

def dist_filter(queryset: BaseManager, address: str, dist_km: int = 20) -> BaseManager:
    user_lat, user_lng = geocode_address(address)
    user_location = GEOSGeometry(f'POINT({user_lng} {user_lat})', srid=4326)
    
    jobs = queryset.filter(
        location__distance_lte=(user_location, D(km=dist_km))
    )
    return jobs