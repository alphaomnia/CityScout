from __future__ import annotations

import io
import math
import zipfile
from xml.etree import ElementTree

import requests

from restaurants.models import RestaurantListing
from .base import BaseRestaurantAdapter

# Only food-service brancheKode prefixes (DD.56.x = serveringsvirksomhed)
# DD.56.10 = restaurants, pizzerias  DD.56.30 = cafes, bars, pubs
FOOD_SERVICE_PREFIX = "DD.56"

# Pixibranche values we accept (belt-and-suspenders filter)
FOOD_PIXI = {
    "Restauranter, pizzeriaer, kantiner m.m.",
    "Cafeer, barer, diskoteker m.m.",
}

# Smiley score: 1=best (happy face), 2=ok, 3=sad, 4=very sad, 0=no score
SMILEY_LABEL = {1: "smiley:1_best", 2: "smiley:2_ok", 3: "smiley:3_sad", 4: "smiley:4_worst"}

# Stable dataset page on Virk datahub — we scrape for the actual resource URL
DATAHUB_URL = "http://datahub.virk.dk/dataset/smiley-kontrolrapporter"
# Known direct URLs to try (the media URL changes periodically)
FALLBACK_URLS = [
    "https://www.foedevarestyrelsen.dk/Media/638212360788086849/Smiley_xml.xml",
    "https://www.foedevarestyrelsen.dk/SiteCollectionDocuments/25_PDF_word_filer%20til%20download/04kontoret/Smiley/smiley_xml.zip",
]


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


class FindSmileyAdapter(BaseRestaurantAdapter):
    name = "findsmiley"

    def fetch(self) -> list[RestaurantListing]:
        xml_bytes = self._download_xml()
        if xml_bytes is None:
            print(f"[{self.name}] Could not download dataset, skipping")
            return []

        center_lat, center_lon = self.city_config["center"]
        radius_km = self.city_config["radius_m"] / 1000.0
        city_name = self.city_config["name"]
        country = self.city_config["country"]

        try:
            root = ElementTree.fromstring(xml_bytes)
        except ElementTree.ParseError as exc:
            print(f"[{self.name}] XML parse error: {exc}")
            return []

        results: list[RestaurantListing] = []
        for row in root.iter("row"):
            t = row.find

            branche_kode = (t("brancheKode") is not None and t("brancheKode").text or "").strip()
            pixi = (t("Pixibranche") is not None and t("Pixibranche").text or "").strip()

            # Keep only restaurants, cafes, bars
            if not branche_kode.startswith(FOOD_SERVICE_PREFIX) and pixi not in FOOD_PIXI:
                continue

            # Coordinates required for city filtering
            try:
                lat = float(t("Geo_Lat").text)
                lon = float(t("Geo_Lng").text)
            except (AttributeError, TypeError, ValueError):
                continue

            if _haversine_km(center_lat, center_lon, lat, lon) > radius_km:
                continue

            name = (t("navn1") is not None and t("navn1").text or "").strip()
            if not name:
                continue

            address_parts = [
                t("adresse1") is not None and t("adresse1").text or "",
                t("postnr") is not None and t("postnr").text or "",
                t("By") is not None and t("By").text or "",
            ]
            address = ", ".join(p.strip() for p in address_parts if p.strip())

            source_id = t("navnelbnr") is not None and t("navnelbnr").text or ""
            url = t("URL") is not None and t("URL").text or ""
            chain = (t("Kaedenavn") is not None and t("Kaedenavn").text or "").strip()
            elite = t("Elite_Smiley") is not None and t("Elite_Smiley").text == "1"

            try:
                score = int(t("seneste_kontrol").text)
            except (AttributeError, TypeError, ValueError):
                score = 0

            tags: list[str] = []
            if score in SMILEY_LABEL:
                tags.append(SMILEY_LABEL[score])
            if elite:
                tags.append("elite_smiley")
            if chain:
                tags.append(f"chain:{chain}")

            cuisine: list[str] = []
            if pixi:
                cuisine.append(pixi)

            results.append(RestaurantListing(
                name=name,
                address=address,
                source=self.name,
                source_id=source_id,
                country=country,
                city=city_name,
                cuisine=cuisine,
                website=url,
                tags=tags,
            ))

        return results

    def _download_xml(self) -> bytes | None:
        # Try to find current URL from datahub page
        try:
            resp = self.session.get(DATAHUB_URL, timeout=15)
            if resp.ok:
                for line in resp.text.splitlines():
                    if "Smiley_xml" in line and "href" in line:
                        import re
                        match = re.search(r'href=["\']([^"\']+Smiley[^"\']+)["\']', line, re.IGNORECASE)
                        if match:
                            url = match.group(1)
                            data = self._fetch_url(url)
                            if data:
                                return data
        except Exception:
            pass

        # Fall back to known URLs
        for url in FALLBACK_URLS:
            data = self._fetch_url(url)
            if data:
                return data

        return None

    def _fetch_url(self, url: str) -> bytes | None:
        try:
            resp = self.session.get(url, timeout=60)
            if not resp.ok:
                return None
            content = resp.content
            # Handle zip archives
            if url.endswith(".zip") or content[:2] == b"PK":
                with zipfile.ZipFile(io.BytesIO(content)) as zf:
                    for name in zf.namelist():
                        if name.lower().endswith(".xml"):
                            return zf.read(name)
                return None
            return content
        except Exception as exc:
            print(f"[{self.name}] Fetch error for {url}: {exc}")
            return None
