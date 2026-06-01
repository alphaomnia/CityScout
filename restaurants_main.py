#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from restaurant_adapters import RESTAURANT_ADAPTERS
from restaurants.config import CITIES
from restaurants.dedup import deduplicate
from restaurants.store import RestaurantStore


def load_config() -> dict:
    path = ROOT / "restaurants_config.yaml"
    return yaml.safe_load(path.read_text("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Restaurant Aggregator")
    parser.add_argument("--initial-scan", action="store_true")
    args = parser.parse_args()
    mode = "bulk" if args.initial_scan else "incremental"

    run_start = datetime.now(timezone.utc)
    print(f"=== Restaurant Aggregator | mode={mode} ===")
    config = load_config()

    store_path = ROOT / config["store"]["path"]
    store = RestaurantStore(store_path)
    existing_count = len(store.all())
    print(f"Loaded {existing_count} existing restaurants from store")

    api_keys = {
        "openstreetmap": "",
    }

    adapters_used = config.get("adapters", [])
    cities_scanned: list[str] = []
    incoming: list = []

    for city_key in config.get("cities", ["prague"]):
        city_cfg = CITIES.get(city_key)
        if city_cfg is None:
            print(f"[main] Unknown city: {city_key!r}, skipping")
            continue
        cities_scanned.append(city_cfg["name"])
        print(f"--- City: {city_cfg['name']} ---")
        for adapter_name in adapters_used:
            cls = RESTAURANT_ADAPTERS.get(adapter_name)
            if cls is None:
                print(f"[main] Unknown adapter: {adapter_name!r}, skipping")
                continue
            adapter = cls(api_key=api_keys.get(adapter_name, ""), mode=mode, city_config=city_cfg)
            incoming.extend(adapter._safe_fetch())
        if mode == "bulk":
            time.sleep(3)  # polite pause between cities to avoid Overpass rate limits

    print(f"Fetched {len(incoming)} raw listings across all sources")
    deduplicated = deduplicate(incoming)
    print(f"After deduplication: {len(deduplicated)} unique listings")

    new_listings = store.merge(deduplicated)
    updated_count = len(deduplicated) - len(new_listings)
    print(f"New restaurants discovered: {len(new_listings)}")

    run_end = datetime.now(timezone.utc)
    duration_s = int((run_end - run_start).total_seconds())
    store.add_changelog_entry({
        "run_at": run_end.isoformat(),
        "mode": mode,
        "duration_s": duration_s,
        "cities_scanned": len(cities_scanned),
        "adapters": adapters_used,
        "fetched_raw": len(incoming),
        "after_dedup": len(deduplicated),
        "new": len(new_listings),
        "updated": updated_count,
        "total": existing_count + len(new_listings),
    })
    store.save()

    dashboard_cfg = config.get("dashboard", {})
    template_path = ROOT / dashboard_cfg.get("template", "docs/_restaurants_template.html")
    output_path = ROOT / dashboard_cfg.get("output", "docs/restaurants.html")
    if template_path.exists():
        output_path.write_text(template_path.read_text("utf-8"), "utf-8")
        print(f"Dashboard regenerated: {output_path}")

    print("=== Done ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
