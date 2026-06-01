from __future__ import annotations

import time
from http.client import IncompleteRead

import requests

from restaurants.config import FOURSQUARE_BASE
from restaurants.models import RestaurantListing
from .base import BaseRestaurantAdapter

RESTAURANT_CATEGORY_ID = "13065"
MAX_RESULTS = 950
FIELDS = "fsq_id,name,location,categories,tel,website,rating,price,hours,photos,stats"
RETRY_DELAYS = [2, 5, 10]  # seconds between retries


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
        rate_limited = False

        while len(results) < MAX_RESULTS:
            params: dict = {
                "query": "restaurant",
                "ll": f"{center[0]},{center[1]}",
                "radius": radius,
                "limit": 50,
                "categories": RESTAURANT_CATEGORY_ID,
                "fields": FIELDS,
            }
            if cursor:
                params["cursor"] = cursor

            resp = self._get_with_retry(
                f"{FOURSQUARE_BASE}/places/search",
                params=params,
                headers=headers,
            )
            if resp is None:
                rate_limited = True
                break

            data = resp.json()
            for place in data.get("results", []):
                listing = self._to_listing(place)
                if listing:
                    results.append(listing)

            cursor = data.get("context", {}).get("next_cursor")
            if not cursor:
                break
            self._sleep(0.5)

        if rate_limited:
            city = self.city_config["name"]
            print(f"[{self.name}/{city}] Rate limit reached — {len(results)} results so far, stopping.")
        elif len(results) >= MAX_RESULTS:
            print(f"[{self.name}] Hit {MAX_RESULTS} result cap")
        return results

    def _get_with_retry(self, url: str, **kwargs) -> requests.Response | None:
        for attempt, delay in enumerate([0] + RETRY_DELAYS):
            if delay:
                self._sleep(delay)
            try:
                resp = self.session.get(url, timeout=self.timeout, **kwargs)
                if resp.status_code == 429:
                    print(f"[{self.name}] 429 rate limit on attempt {attempt + 1}")
                    continue
                if resp.status_code == 401:
                    print(f"[{self.name}] 401 Unauthorized — invalid API key or quota exhausted")
                    return None
                resp.raise_for_status()
                return resp
            except (requests.exceptions.ChunkedEncodingError, IncompleteRead, ConnectionError) as exc:
                print(f"[{self.name}] Connection error attempt {attempt + 1}: {exc}")
                continue
            except requests.RequestException as exc:
                print(f"[{self.name}] Request error: {exc}")
                return None
        print(f"[{self.name}] All retries exhausted")
        return None

    def _to_listing(self, place: dict) -> RestaurantListing | None:
        name = place.get("name", "").strip()
        if not name:
            return None

        location = place.get("location", {})
        address = ", ".join(p for p in [
            location.get("address", ""),
            location.get("locality", ""),
            location.get("region", ""),
        ] if p) or self.city_config["osm_name"]

        fsq_id = place.get("fsq_id", "")
        raw_rating = place.get("rating", 0.0)
        neighborhood = (
            location.get("neighborhood", [""])[0]
            if isinstance(location.get("neighborhood"), list)
            else location.get("neighborhood", "")
        )

        hours_data = place.get("hours", {})
        oh: dict = {}
        if hours_data:
            display = hours_data.get("display", "")
            open_now = hours_data.get("open_now")
            if display:
                oh["raw"] = display
            if open_now is not None:
                oh["open_now"] = open_now

        photos = []
        for p in place.get("photos", [])[:3]:
            prefix = p.get("prefix", "")
            suffix = p.get("suffix", "")
            if prefix and suffix:
                photos.append(f"{prefix}400x300{suffix}")

        return RestaurantListing(
            name=name,
            address=address,
            source="foursquare",
            source_id=fsq_id,
            country=self.city_config["country"],
            city=self.city_config["name"],
            neighborhood=neighborhood,
            cuisine=[cat["name"] for cat in place.get("categories", []) if cat.get("name")],
            price_level=place.get("price", 0) or 0,
            rating=round(raw_rating / 2, 1) if raw_rating else 0.0,
            review_count=place.get("stats", {}).get("total_ratings", 0) or 0,
            phone=place.get("tel", ""),
            website=place.get("website", ""),
            google_maps_url=f"https://foursquare.com/v/{fsq_id}" if fsq_id else "",
            opening_hours=oh,
            photos=photos,
        )
