from .base import BaseRestaurantAdapter
from .openstreetmap import OpenStreetMapAdapter

RESTAURANT_ADAPTERS: dict[str, type[BaseRestaurantAdapter]] = {
    "openstreetmap": OpenStreetMapAdapter,
}
