from __future__ import annotations

from restaurants.config import (
    GOOGLE_DETAIL_FIELDS_ATMOSPHERE, GOOGLE_DETAIL_FIELDS_BASIC,
    GOOGLE_DETAIL_FIELDS_CONTACT, GOOGLE_PLACES_BASE,
)
from restaurants.models import RestaurantListing
from .base import BaseRestaurantAdapter

_SKIP_TYPES = {"restaurant", "food", "point_of_interest", "establishment", "meal_takeaway", "meal_delivery", "store", "bar", "cafe"}


def _types_to_cuisine(types: list[str]) -> list[str]:
    return [t.replace("_restaurant", "").replace("_", " ").title() for t in types if t not in _SKIP_TYPES]


def _extract_neighborhood(address_components: list[dict]) -> str:
    for comp in address_components:
        types = comp.get("types", [])
        if "sublocality_level_1" in types or "neighborhood" in types:
            return comp.get("long_name", "")
    return ""


class GooglePlacesAdapter(BaseRestaurantAdapter):
    name = "google_places"

    def fetch(self) -> list[RestaurantListing]:
        if not self.api_key:
            print(f"[{self.name}] No API key set — skipping")
            return []
        return self._bulk_scan() if self.mode == "bulk" else self._incremental()

    def _bulk_scan(self) -> list[RestaurantListing]:
        city_name = self.city_config["name"]
        queries = [f"restaurants in {d}" for d in self.city_config["districts"]]
        queries += [f"restaurants in {n}, {city_name}" for n in self.city_config["neighborhoods"]]
        return self._run_text_searches(queries)

    def _incremental(self) -> list[RestaurantListing]:
        districts = self.city_config["districts"]
        nearby = self._nearby_search()
        text = self._run_text_searches([f"restaurants in {districts[0]}", f"restaurants in {districts[1]}"])
        seen_ids: set[str] = set()
        results: list[RestaurantListing] = []
        for listing in nearby + text:
            if listing.source_id not in seen_ids:
                seen_ids.add(listing.source_id)
                results.append(listing)
        return results

    def _run_text_searches(self, queries: list[str]) -> list[RestaurantListing]:
        seen_place_ids: set[str] = set()
        results: list[RestaurantListing] = []
        for query in queries:
            for place in self._text_search(query):
                pid = place.get("place_id", "")
                if not pid or pid in seen_place_ids:
                    continue
                seen_place_ids.add(pid)
                listing = self._to_listing(place, self._place_details(pid))
                if listing:
                    results.append(listing)
                self._sleep(0.1)
        return results

    def _text_search(self, query: str) -> list[dict]:
        url = f"{GOOGLE_PLACES_BASE}/textsearch/json"
        places: list[dict] = []
        params = {"query": query, "type": "restaurant", "key": self.api_key}
        for _ in range(3):
            resp = self._get(url, params=params)
            if not resp:
                break
            data = resp.json()
            if data.get("status") not in ("OK", "ZERO_RESULTS"):
                break
            places.extend(data.get("results", []))
            token = data.get("next_page_token")
            if not token:
                break
            self._sleep(2)
            params = {"pagetoken": token, "key": self.api_key}
        return places

    def _nearby_search(self) -> list[dict]:
        url = f"{GOOGLE_PLACES_BASE}/nearbysearch/json"
        center = self.city_config["center"]
        radius = self.city_config["radius_m"]
        places: list[dict] = []
        params = {"location": f"{center[0]},{center[1]}", "radius": radius, "type": "restaurant", "rankby": "prominence", "key": self.api_key}
        for _ in range(3):
            resp = self._get(url, params=params)
            if not resp:
                break
            data = resp.json()
            if data.get("status") not in ("OK", "ZERO_RESULTS"):
                break
            places.extend(data.get("results", []))
            token = data.get("next_page_token")
            if not token:
                break
            self._sleep(2)
            params = {"pagetoken": token, "key": self.api_key}
        return places

    def _place_details(self, place_id: str) -> dict:
        url = f"{GOOGLE_PLACES_BASE}/details/json"
        all_fields = ",".join([GOOGLE_DETAIL_FIELDS_BASIC, GOOGLE_DETAIL_FIELDS_CONTACT, GOOGLE_DETAIL_FIELDS_ATMOSPHERE])
        resp = self._get(url, params={"place_id": place_id, "fields": all_fields, "key": self.api_key})
        return resp.json().get("result", {}) if resp else {}

    def _to_listing(self, place: dict, details: dict) -> RestaurantListing | None:
        src = details if details else place
        name = src.get("name", "").strip()
        if not name or src.get("permanently_closed"):
            return None
        place_id = place.get("place_id", "")
        oh_data = src.get("opening_hours", {})
        photos = []
        for photo in src.get("photos", [])[:3]:
            ref = photo.get("photo_reference", "")
            if ref:
                photos.append(f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={ref}&key={self.api_key}")
        return RestaurantListing(
            name=name,
            address=src.get("formatted_address", place.get("formatted_address", "")),
            source="google_places",
            source_id=place_id,
            country=self.city_config["country"],
            city=self.city_config["name"],
            neighborhood=_extract_neighborhood(src.get("address_components", [])),
            cuisine=_types_to_cuisine(src.get("types", [])),
            price_level=int(src.get("price_level", 0) or 0),
            rating=float(src.get("rating", 0.0) or 0.0),
            review_count=int(src.get("user_ratings_total", 0) or 0),
            phone=src.get("formatted_phone_number", ""),
            website=src.get("website", ""),
            google_maps_url=f"https://www.google.com/maps/place/?q=place_id:{place_id}" if place_id else "",
            opening_hours={"weekday_text": oh_data.get("weekday_text", []), "open_now": oh_data.get("open_now")} if oh_data else {},
            photos=photos,
        )
