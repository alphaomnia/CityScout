"""
One-off import: malta_venues_for_aggregator.csv → candidate stubs
Handles the Malta-specific column schema (different from DBExport.csv).
"""
import csv, json, re, sqlite3, uuid
from datetime import datetime, timezone
from pathlib import Path

DB_PATH  = Path(__file__).parent / "cityscout.db"
CSV_PATH = Path(__file__).parent.parent / "malta_venues_for_aggregator.csv"

def now():
    return datetime.now(timezone.utc).isoformat()

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")

def run():
    db = sqlite3.connect(DB_PATH, timeout=15)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")

    # ── Source record ──────────────────────────────────────────────────────────
    source_name = "Malta-1.pdf (CityScout Malta guide)"
    existing_src = db.execute(
        "SELECT source_id FROM source WHERE source_name=?", (source_name,)
    ).fetchone()

    if existing_src:
        source_id = existing_src["source_id"]
        print(f"Reusing existing source: {source_id}")
    else:
        source_id = str(uuid.uuid4())
        db.execute("""
            INSERT INTO source
              (source_id, source_name, source_type, coverage_city, coverage_country,
               source_url_or_file, source_origin, approval_status, quality_grade,
               why_this_grade, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (
            source_id, source_name, "book", "Malta (multiple)", "Malta",
            "malta_venues_for_aggregator.csv", "print_guide",
            "approved", "silver",
            "Print guidebook extract, structured by local area, manually parsed",
            now(),
        ))
        print(f"Created source: {source_id}")

    created = skipped = updated_existing = 0

    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name", "").strip()
            if not name:
                skipped += 1
                continue

            # Deduplicate by canonical name + city
            city = row.get("locality", "").strip()
            existing = db.execute(
                "SELECT candidate_id FROM candidate WHERE canonical_name=? AND city=?",
                (name, city)
            ).fetchone()
            if existing:
                print(f"  SKIP (exists): {name} / {city}")
                skipped += 1
                continue

            # Field mapping
            venue_type = row.get("venue_type", "").strip()
            section    = row.get("section", "").strip()
            address    = row.get("street_address", "").strip()
            island     = row.get("island", "").strip()
            country    = "Malta"

            lat_s = row.get("latitude", "").strip()
            lng_s = row.get("longitude", "").strip()
            lat   = float(lat_s) if lat_s else None
            lng   = float(lng_s) if lng_s else None

            description   = row.get("description", "").strip()
            flags         = row.get("flags_notes", "").strip()
            website       = row.get("website_corrected", "").strip() or row.get("website_printed", "").strip()
            phone         = row.get("phone", "").strip()
            parse_conf    = row.get("parse_confidence", "high").strip()
            area_flag     = row.get("area_or_cluster", "no").strip().lower() == "yes"

            # Build tags from section, island, area flag, website, phone
            tags = []
            if section:
                tags.append(section)
            if island and island.lower() not in ("malta",):
                tags.append(island)
            if area_flag:
                tags.append("multi-venue area")
            if phone:
                tags.append(f"tel:{phone}")
            if website:
                tags.append(f"web:{website}")

            # Confidence → tier mapping
            tier_map = {"high": "tier2", "medium": "tier3", "low": "tier4"}
            tier = tier_map.get(parse_conf, "tier3")

            slug         = slugify(name) + "-malta"
            candidate_id = str(uuid.uuid4())
            claim_id     = str(uuid.uuid4())
            decision_id  = str(uuid.uuid4())

            db.execute("""
                INSERT INTO candidate
                  (candidate_id, canonical_name, city, country, neighborhood,
                   google_place_id_or_url, address, lat, lng,
                   candidate_status, inclusion_status, publish_status,
                   source_count, primary_source_id,
                   category, description, tags, slug, tier,
                   created_from, created_at, updated_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                candidate_id, name, city, country,
                island if island.lower() not in ("malta",) else None,
                website or None,
                address or None,
                lat, lng,
                "stub", "pending", "unpublished",
                1, source_id,
                venue_type or None,
                description or None,
                json.dumps(tags),
                slug, tier,
                "malta_guide_import",
                now(), now(),
            ))

            db.execute("""
                INSERT INTO source_claim
                  (claim_id, source_id, raw_place_name, city, country,
                   claimed_address, claimed_category_tags,
                   source_confidence, parse_confidence,
                   candidate_id, poi_match_status, created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                claim_id, source_id, name, city, country,
                address or None,
                json.dumps([venue_type] if venue_type else []),
                0.75,
                0.9 if parse_conf == "high" else (0.7 if parse_conf == "medium" else 0.5),
                candidate_id, "unresolved", now(),
            ))

            db.execute("""
                INSERT INTO decision_log
                  (decision_id, candidate_id, previous_status, new_status,
                   decision_type, reason, decider, created_at)
                VALUES (?,?,?,?,?,?,?,?)
            """, (
                decision_id, candidate_id, None, "stub",
                "candidate_created",
                f"Imported from Malta print guide (Malta-1.pdf). Section: {section}. Flags: {flags}",
                "malta_guide_import",
                now(),
            ))

            print(f"  + {name} / {city}")
            created += 1

    db.commit()
    db.close()

    print(f"\n✓ Done — created: {created}, skipped: {skipped}")

if __name__ == "__main__":
    run()
