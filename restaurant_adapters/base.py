from __future__ import annotations

import time
from abc import ABC, abstractmethod

import requests

from restaurants.config import CITIES
from restaurants.models import RestaurantListing

USER_AGENT = "cityscout/1.0 (Czech restaurant discovery; github.com/alphaomnia/CityScout)"


class BaseRestaurantAdapter(ABC):
    name: str = ""
    timeout: int = 30

    def __init__(self, api_key: str = "", mode: str = "incremental", city_config: dict | None = None) -> None:
        self.api_key = api_key
        self.mode = mode
        self.city_config = city_config or CITIES["prague"]
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

    @abstractmethod
    def fetch(self) -> list[RestaurantListing]: ...

    def _get(self, url: str, **kwargs) -> requests.Response | None:
        kwargs.setdefault("timeout", self.timeout)
        try:
            resp = self.session.get(url, **kwargs)
            resp.raise_for_status()
            return resp
        except requests.RequestException as exc:
            print(f"[{self.name}] GET {url} failed: {exc}")
            return None

    def _post(self, url: str, **kwargs) -> requests.Response | None:
        kwargs.setdefault("timeout", self.timeout)
        try:
            resp = self.session.post(url, **kwargs)
            resp.raise_for_status()
            return resp
        except requests.RequestException as exc:
            print(f"[{self.name}] POST {url} failed: {exc}")
            return None

    def _safe_fetch(self) -> list[RestaurantListing]:
        city_name = self.city_config.get("name", "?")
        try:
            results = self.fetch()
            print(f"[{self.name}/{city_name}] Fetched {len(results)} listings (mode={self.mode})")
            return results
        except Exception as exc:
            print(f"[{self.name}/{city_name}] Adapter error: {exc}")
            return []

    def _sleep(self, seconds: float) -> None:
        time.sleep(seconds)
