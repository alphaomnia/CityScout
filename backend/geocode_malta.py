"""
Geocode Malta candidates that have no lat/lng using Nominatim (OpenStreetMap).
Rate-limited to 1 req/sec as required by Nominatim's usage policy.
"""
import json, sqlite3, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

DB_PATH   = Path(__file__).parent / "cityscout.db"
NOM_BASE  = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "CityScout/1.0 (info@reubenchircop.com)"

def now():
    return datetime.now(timezone.utc).isoformat()

def geocode(query: str) -> tuple[float, float] | None:
    params = urllib.parse.urlencode({
        "q": query,
        "format": "jsonv2",
        "limit": 1,
        "countrycodes": "mt",
    })
    url = f"{NOM_BASE}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception as e:
        print(f"    HTTP error: {e}")
    return None

def try_queries(name: str, city: str, address: str) -> tuple[float, float, str] | None:
    """Try progressively broader queries until one hits."""
    attempts = []

    # Most specific: address + city
    if address:
        attempts.append((f"{address}, {city}, Malta", "address+city"))

    # Name + address
    if address:
        attempts.append((f"{name}, {address}, {city}, Malta", "name+address+city"))

    # Name + city
    attempts.append((f"{name}, {city}, Malta", "name+city"))

    # Name + Malta only (for venues in Gozo or small localities)
    attempts.append((f"{name}, Malta", "name+country"))

    for query, label in attempts:
        time.sleep(1.1)   # Nominatim: max 1 req/sec
        result = geocode(query)
        if result:
            return result[0], result[1], label

    return None

def run():
    db = sqlite3.connect(DB_PATH, timeout=15)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")

    rows = db.execute("""
        SELECT candidate_id, canonical_name, city, address, country
        FROM candidate
        WHERE country='Malta' AND (lat IS NULL OR lat=0)
        ORDER BY city, canonical_name
    """).fetchall()

    print(f"Geocoding {len(rows)} Malta venues via Nominatim…\n")
    found = failed = 0

    for row in rows:
        name    = row["canonical_name"]
        city    = row["city"] or ""
        address = row["address"] or ""

        print(f"  [{found+failed+1}/{len(rows)}] {name} / {city}")
        result = try_queries(name, city, address)

        if result:
            lat, lng, method = result
            db.execute(
                "UPDATE candidate SET lat=?, lng=?, updated_at=? WHERE candidate_id=?",
                (lat, lng, now(), row["candidate_id"])
            )
            db.commit()
            print(f"    ✓ {lat:.5f}, {lng:.5f}  [{method}]")
            found += 1
        else:
            print(f"    ✗ Not found")
            failed += 1

    db.close()
    print(f"\n✓ Done — geocoded: {found}, failed: {failed}")

if __name__ == "__main__":
    run()
