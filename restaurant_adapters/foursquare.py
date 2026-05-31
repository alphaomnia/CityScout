from __future__ import annotations

from restaurants.config import FOURSQUARE_BASE
from restaurants.models import RestaurantListing
from .base import BaseRestaurantAdapter

RESTAURANT_CATEGORY_ID = "13065"
MAX_RESULTS = 950


class FoursquareAdapter(BaseRestaurantAdapter):
    name = "foursquare"

    def fetch(self) -> list[RestaurantListing]:
        if not self.api_key:
            print(f"[{self.name}] No API key, skipping")
            return []

        center = self.city_config["center"]
        radius = self.city_config["radius_m"]
        results: list[RestaurantListing] = []
        cursor: str | None = None
        headers = {"Authorization": self.api_key, "Accept": "application/json"}

        while len(results) < MAX_RESULTS:
            params: dict = {
                "query": "restaurant",
                "ll": f"{center[0]},{center[1]}",
                "radius": radius,
                "limit": 50,
                "categories": RESTAURANT_CATEGORY_ID,
            }
            if cursor:
                params["cursor"] = cursor

            resp = self._get(f"{FOURSQUARE_BASE}/places/search", params=params, headers=headers)
            if not resp:
                break

            data = resp.json()
            for place in data.get("results", []):
                listing = self._to_listing(place)
                if listing:
                    results.append(listing)

            cursor = data.get("context", {}).get("next_cursor")
            if not cursor:
                break
            self._sleep(0.2)

        if len(results) >= MAX_RESULTS:
            print(f"[{self.name}] Hit {MAX_RESULTS} result cap")
        return results

    def _to_listing(self, place: dict) -> RestaurantListing | None:
        name = place.get("name", "").strip()
        if not name:
            return None

        location = place.get("location", {})
        address = ", ".join(p for p in [
            location.get("address", ""), location.get("locality", ""), location.get("region", "")
        ] if p) or self.city_config["osm_name"]
        fsq_id = place.get("fsq_id", "")
        raw_rating = place.get("rating", 0.0)
        neighborhood = location.get("neighborhood", [""])[0] if isinstance(location.get("neighborhood"), list) else location.get("neighborhood", "")

        return RestaurantListing(
            name=name,
            address=address,
            source="foursquare",
            source_id=fsq_id,
            country=self.city_config["country"],
            city=self.city_config["name"],
            neighborhood=neighborhood,
            cuisine=[cat["name"] for cat in place.get("categories", []) if cat.get("name")],
            price_level=place.get("price", 0),
            rating=round(raw_rating / 2, 1) if raw_rating else 0.0,
            phone=place.get("tel", ""),
            website=place.get("website", ""),
            google_maps_url=f"https://foursquare.com/v/{fsq_id}" if fsq_id else "",
        )
