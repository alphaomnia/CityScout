from __future__ import annotations

import time

import requests

from restaurants.config import OVERPASS_URL
from restaurants.models import RestaurantListing
from .base import BaseRestaurantAdapter

OVERPASS_QUERY = """
[out:json][timeout:60];
(
  node["amenity"="restaurant"]({south},{west},{north},{east});
  way["amenity"="restaurant"]({south},{west},{north},{east});
  relation["amenity"="restaurant"]({south},{west},{north},{east});
  node["amenity"="cafe"]({south},{west},{north},{east});
  way["amenity"="cafe"]({south},{west},{north},{east});
  node["amenity"="bar"]({south},{west},{north},{east});
  way["amenity"="bar"]({south},{west},{north},{east});
  node["amenity"="pub"]({south},{west},{north},{east});
  way["amenity"="pub"]({south},{west},{north},{east});
);
out body center;
"""

RETRY_DELAYS = [5, 15, 30]
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

        resp = self._post_with_retry(query)
        if not resp:
            return []

        listings = []
        for el in resp.json().get("elements", []):
            listing = self._to_listing(el)
            if listing:
                listings.append(listing)
        return listings

    def _post_with_retry(self, query: str) -> requests.Response | None:
        for attempt, delay in enumerate([0] + RETRY_DELAYS):
            if delay:
                print(f"[{self.name}] Waiting {delay}s before retry {attempt}...")
                time.sleep(delay)
            try:
                resp = self.session.post(OVERPASS_URL, data={"data": query}, timeout=75)
                if resp.status_code == 429:
                    print(f"[{self.name}] Rate limited (429), will retry")
                    continue
                if resp.status_code == 504:
                    print(f"[{self.name}] Gateway timeout (504), will retry")
                    continue
                resp.raise_for_status()
                return resp
            except requests.RequestException as exc:
                print(f"[{self.name}] Request error attempt {attempt + 1}: {exc}")
                continue
        print(f"[{self.name}] All retries exhausted")
        return None

    def _to_listing(self, el: dict) -> RestaurantListing | None:
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
        amenity = tags.get("amenity", "restaurant")
        venue_tags = [f"osm:{el['type']}/{el['id']}"]
        if amenity != "restaurant":
            venue_tags.append(f"type:{amenity}")

        return RestaurantListing(
            name=name,
            address=address,
            source="openstreetmap",
            source_id=f"{el['type']}/{el['id']}",
            country=self.city_config["country"],
            city=self.city_config["name"],
            neighborhood=tags.get("addr:suburb", tags.get("addr:quarter", "")),
            cuisine=_parse_cuisine(tags.get("cuisine", "")),
            phone=tags.get("phone", tags.get("contact:phone", "")),
            website=tags.get("website", tags.get("contact:website", "")),
            opening_hours={"raw": oh_raw} if oh_raw else {},
            tags=venue_tags,
        )
