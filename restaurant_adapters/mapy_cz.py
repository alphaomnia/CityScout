from __future__ import annotations

from restaurants.config import PRAGUE_CENTER, PRAGUE_SEARCH_RADIUS_M
from restaurants.models import RestaurantListing
from .base import BaseRestaurantAdapter

MAPY_CZ_BASE = "https://api.mapy.cz/v1"
MAX_RESULTS = 500
PAGE_SIZE = 15  # Mapy.cz max per request


class MapyCzAdapter(BaseRestaurantAdapter):
    name = "mapy_cz"

    def fetch(self) -> list[RestaurantListing]:
        if not self.api_key:
            print(f"[{self.name}] No API key, skipping")
            return []

        results: list[RestaurantListing] = []
        offset = 0

        while len(results) < MAX_RESULTS:
            params = {
                "query": "restaurant",
                "lat": PRAGUE_CENTER[0],
                "lon": PRAGUE_CENTER[1],
                "radius": PRAGUE_SEARCH_RADIUS_M,
                "limit": PAGE_SIZE,
                "offset": offset,
                "lang": "en",
                "apikey": self.api_key,
            }
            resp = self._get(f"{MAPY_CZ_BASE}/places/search", params=params)
            if not resp:
                break

            data = resp.json()
            items = data.get("items", [])
            if not items:
                break

            for item in items:
                listing = self._to_listing(item)
                if listing:
                    results.append(listing)

            if len(items) < PAGE_SIZE:
                break
            offset += PAGE_SIZE
            self._sleep(0.15)

        return results

    def _to_listing(self, item: dict) -> RestaurantListing | None:
        name = item.get("name", "").strip()
        if not name:
            return None

        location = item.get("location", {})
        parts = [
            location.get("streetAddress", ""),
            location.get("municipalityName", ""),
        ]
        address = ", ".join(p for p in parts if p) or "Praha"

        mapy_id = str(item.get("id", ""))
        url = f"https://mapy.cz/zakladni?source=firm&id={mapy_id}" if mapy_id else ""

        contact = item.get("contact", {})
        cats = [c.get("name", "") for c in item.get("categories", []) if c.get("name")]

        return RestaurantListing(
            name=name,
            address=address,
            source="mapy_cz",
            source_id=mapy_id,
            neighborhood=location.get("quarterName", location.get("districtName", "")),
            cuisine=cats,
            phone=contact.get("phone", ""),
            website=contact.get("url", ""),
            google_maps_url=url,
            rating=float(item.get("rating", 0.0) or 0.0),
            review_count=int(item.get("ratingCount", 0) or 0),
        )
