from .base import BaseRestaurantAdapter
from .openstreetmap import OpenStreetMapAdapter
from .findsmiley import FindSmileyAdapter

RESTAURANT_ADAPTERS: dict[str, type[BaseRestaurantAdapter]] = {
    "openstreetmap": OpenStreetMapAdapter,
    "findsmiley": FindSmileyAdapter,
}
