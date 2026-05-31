from __future__ import annotations

from restaurants.models import RestaurantListing
from .base import BaseRestaurantAdapter

HERE_BASE = "https://discover.search.hereapi.com/v1"
MAX_RESULTS = 1000
PAGE_SIZE = 100  # HERE maximum per request


class HereAdapter(BaseRestaurantAdapter):
    name = "here"

    def fetch(self) -> list[RestaurantListing]:
        if not self.api_key:
            print(f"[{self.name}] No API key, skipping")
            return []

        center = self.city_config["center"]
        bbox = self.city_config["bbox"]
        results: list[RestaurantListing] = []
        next_url: str | None = None

        # HERE uses a bounding box or at= with limit — we use bbox for accuracy
        base_params = {
            "in": f"bbox:{bbox['west']},{bbox['south']},{bbox['east']},{bbox['north']}",
            "q": "restaurant",
            "limit": PAGE_SIZE,
            "apiKey": self.api_key,
        }

        while len(results) < MAX_RESULTS:
            if next_url:
                resp = self._get(next_url)
            else:
                resp = self._get(f"{HERE_BASE}/discover", params=base_params)

            if not resp:
                break

            data = resp.json()
            for item in data.get("items", []):
                listing = self._to_listing(item)
                if listing:
                    results.append(listing)

            next_href = data.get("next")
            if not next_href:
                break
            # append apiKey to next page URL
            next_url = next_href + ("&" if "?" in next_href else "?") + f"apiKey={self.api_key}"
            self._sleep(0.1)

        return results

    def _to_listing(self, item: dict) -> RestaurantListing | None:
        name = item.get("title", "").strip()
        if not name:
            return None

        address = item.get("address", {})
        addr_str = ", ".join(p for p in [
            address.get("street", ""),
            address.get("houseNumber", ""),
            address.get("city", ""),
        ] if p) or self.city_config["osm_name"]

        here_id = item.get("id", "")
        position = item.get("position", {})
        lat = position.get("lat", "")
        lng = position.get("lng", "")
        maps_url = f"https://maps.here.com/?q={lat},{lng}" if lat and lng else ""

        # categories -> cuisine
        cuisine = []
        for cat in item.get("categories", []):
            cat_name = cat.get("name", "")
            if cat_name and cat_name.lower() not in {"restaurant", "food & drink", "food"}:
                cuisine.append(cat_name)

        # contacts
        contacts = item.get("contacts", [])
        phone, website = "", ""
        for contact in contacts:
            for ph in contact.get("phone", []):
                if not phone:
                    phone = ph.get("value", "")
            for www in contact.get("www", []):
                if not website:
                    website = www.get("value", "")

        # opening hours
        oh: dict = {}
        hours_list = item.get("openingHours", [])
        if hours_list:
            raw_text = "; ".join(
                text
                for h in hours_list
                for text in h.get("text", [])
            )
            if raw_text:
                oh["raw"] = raw_text
            is_open = hours_list[0].get("isOpen")
            if is_open is not None:
                oh["open_now"] = is_open

        neighborhood = address.get("district", address.get("subdistrict", ""))

        return RestaurantListing(
            name=name,
            address=addr_str,
            source="here",
            source_id=here_id,
            country=self.city_config["country"],
            city=self.city_config["name"],
            neighborhood=neighborhood,
            cuisine=cuisine,
            phone=phone,
            website=website,
            google_maps_url=maps_url,
            opening_hours=oh,
        )
