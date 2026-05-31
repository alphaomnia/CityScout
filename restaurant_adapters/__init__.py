from .base import BaseRestaurantAdapter
from .google_places import GooglePlacesAdapter
from .openstreetmap import OpenStreetMapAdapter
from .foursquare import FoursquareAdapter
from .mapy_cz import MapyCzAdapter

RESTAURANT_ADAPTERS: dict[str, type[BaseRestaurantAdapter]] = {
    "google_places": GooglePlacesAdapter,
    "openstreetmap": OpenStreetMapAdapter,
    "foursquare": FoursquareAdapter,
    "mapy_cz": MapyCzAdapter,
}
