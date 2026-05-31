from __future__ import annotations

from restaurants.config import OVERPASS_URL
from restaurants.models import RestaurantListing
from .base import BaseRestaurantAdapter

OVERPASS_QUERY = """
[out:json][timeout:90];
(
  node["amenity"="restaurant"]({south},{west},{north},{east});
  way["amenity"="restaurant"]({south},{west},{north},{east});
  relation["amenity"="restaurant"]({south},{west},{north},{east});
);
out body center;
"""

_SKIP_CUISINES = {"yes", "no", "other", "international", "regional", "traditional"}


def _parse_cuisine(raw: str) -> list[str]:
    parts = [p.strip() for p in raw.split(";") if p.strip()]
    result = []
    for part in parts:
        if part.lower() in _SKIP_CUISINES:
            continue
        cleaned = part.replace("_", " ").strip().title()
        if cleaned:
            result.append(cleaned)
    return result


class OpenStreetMapAdapter(BaseRestaurantAdapter):
    name = "openstreetmap"

    def fetch(self) -> list[RestaurantListing]:
        if self.mode == "incremental":
            print(f"[{self.name}] Skipping in incremental mode")
            return []

        bbox = self.city_config["bbox"]
        query = OVERPASS_QUERY.format(
            south=bbox["south"], west=bbox["west"],
            north=bbox["north"], east=bbox["east"],
        )
        resp = self._post(OVERPASS_URL, data={"data": query})
        if not resp:
            return []

        city_name = self.city_config["name"]
        listings = []
        for el in resp.json().get("elements", []):
            listing = self._to_listing(el, city_name)
            if listing:
                listings.append(listing)
        return listings

    def _to_listing(self, el: dict, city_name: str) -> RestaurantListing | None:
        tags = el.get("tags", {})
        name = tags.get("name", "").strip()
        if not name:
            return None

        street = tags.get("addr:street", "")
        house_num = tags.get("addr:housenumber", "")
        city = tags.get("addr:city", self.city_config["osm_name"])
        if street and house_num:
            address = f"{street} {house_num}, {city}"
        elif street:
            address = f"{street}, {city}"
        else:
            address = city

        oh_raw = tags.get("opening_hours", "")
        return RestaurantListing(
            name=name,
            address=address,
            source="openstreetmap",
            source_id=f"{el['type']}/{el['id']}",
            city=city_name,
            neighborhood=tags.get("addr:suburb", tags.get("addr:quarter", "")),
            cuisine=_parse_cuisine(tags.get("cuisine", "")),
            phone=tags.get("phone", tags.get("contact:phone", "")),
            website=tags.get("website", tags.get("contact:website", "")),
            opening_hours={"raw": oh_raw} if oh_raw else {},
            tags=[f"osm:{el['type']}/{el['id']}"],
        )
