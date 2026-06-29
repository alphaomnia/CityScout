"""
Corpus import worker — Green 1 seed.
Imports existing published Prague venues from DBExport.csv as candidates.
Creates: 1 source record, N candidate records, N source_claims, N decision_logs, 1 job_run.
"""
import csv, json, sqlite3, uuid, sys
from datetime import datetime, timezone
from pathlib import Path

DB_PATH  = Path(__file__).parent / "cityscout.db"
CSV_PATH = Path(__file__).parent.parent / "DBExport.csv"
COORDS_PATH = Path(__file__).parent.parent / "query-results-export-2026-06-27_01-42-46.csv"

def now():
    return datetime.now(timezone.utc).isoformat()

def run():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    schema = (Path(__file__).parent / "schema.sql").read_text()
    db.executescript(schema)

    run_id   = str(uuid.uuid4())
    batch_id = str(uuid.uuid4())
    t_start  = datetime.now(timezone.utc)

    created = updated = skipped = errors = 0
    error_msgs = []

    # ── Load real coordinates ───────────────────────────────────────────────
    coords = {}  # name → list of {lat, lng}
    with open(COORDS_PATH, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter=';'):
            name = row['name'].strip()
            try:
                lat = float(row['coordinates_lat'])
                lng = float(row['coordinates_lng'])
                coords.setdefault(name, []).append({'lat': lat, 'lng': lng})
            except ValueError:
                pass

    # ── Create or retrieve source record ───────────────────────────────────
    existing_src = db.execute(
        "SELECT source_id FROM source WHERE source_name=?", ("DBExport.csv",)
    ).fetchone()

    if existing_src:
        source_id = existing_src["source_id"]
        print("Source record already exists — reusing.")
    else:
        source_id = str(uuid.uuid4())
        db.execute("""
            INSERT INTO source
              (source_id, source_name, source_type, coverage_city, coverage_country,
               source_url_or_file, source_origin, approval_status, quality_grade,
               why_this_grade, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (
            source_id, "DBExport.csv", "sheet", "Prague", "Czech Republic",
            "DBExport.csv", "offline_photo", "approved", "gold",
            "First-hand founder-verified corpus, Prague ecosystem",
            now(),
        ))
        print(f"Created source: {source_id}")

    # ── Import venues ──────────────────────────────────────────────────────
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name    = row['name'].strip()
            status  = row.get('status', 'published').strip()
            slug    = row.get('slug', '').strip()
            tier    = row.get('tier', '').strip()
            if status != 'published':
                skipped += 1
                continue

            # Check dedupe
            existing = db.execute(
                "SELECT candidate_id, candidate_status FROM candidate WHERE slug=? OR canonical_name=?",
                (slug, name)
            ).fetchone()
            if existing:
                skipped += 1
                continue

            # Coordinates
            coord_list = coords.get(name, [])
            coord      = coord_list.pop(0) if coord_list else None
            lat  = coord['lat'] if coord else None
            lng  = coord['lng'] if coord else None

            try:
                tags = json.loads(row.get('tags', '') or '[]')
            except Exception:
                tags = []

            candidate_id = str(uuid.uuid4())
            claim_id     = str(uuid.uuid4())
            decision_id  = str(uuid.uuid4())

            # Map tier → candidate_status
            # These are already published — start them at published
            cand_status = 'published'

            db.execute("""
                INSERT INTO candidate
                  (candidate_id, canonical_name, city, country, neighborhood,
                   address, lat, lng, candidate_status, inclusion_status,
                   publish_status, source_count, primary_source_id,
                   category, food_type, dining_type, seating, description,
                   image_url, tags, slug, tier, created_from, created_at, updated_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                candidate_id, name,
                row.get('city', 'Prague').strip(),
                row.get('country', 'Czech Republic').strip(),
                None,
                row.get('address', '').strip(),
                lat, lng,
                cand_status, 'include', 'published',
                1, source_id,
                row.get('category', '').strip(),
                row.get('food_type', '').strip(),
                row.get('dining_type', '').strip(),
                row.get('seating', '').strip(),
                row.get('description', '').strip(),
                row.get('image_url', '').strip(),
                json.dumps(tags),
                slug, tier,
                'worker',
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
                claim_id, source_id, name,
                row.get('city', 'Prague').strip(),
                row.get('country', 'Czech Republic').strip(),
                row.get('address', '').strip(),
                json.dumps(tags),
                0.95, 0.95,
                candidate_id, 'matched', now(),
            ))

            db.execute("""
                INSERT INTO decision_log
                  (decision_id, candidate_id, previous_status, new_status,
                   decision_type, reason, decider, created_at)
                VALUES (?,?,?,?,?,?,?,?)
            """, (
                decision_id, candidate_id, None, 'published',
                'candidate_created',
                'Seeded from founder-verified corpus (DBExport.csv)',
                'corpus_import_worker',
                now(),
            ))

            created += 1

    # ── Log the job run ────────────────────────────────────────────────────
    elapsed = (datetime.now(timezone.utc) - t_start).total_seconds()
    db.execute("""
        INSERT INTO job_run
          (job_run_id, worker_name, input_type, input_id, batch_id,
           status, severity, created_count, skipped_count, error_count,
           error_summary, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        run_id, 'corpus_import_worker', 'csv', str(CSV_PATH), batch_id,
        'success' if not errors else 'partial',
        'info' if not errors else 'warning',
        created, skipped, errors,
        '; '.join(error_msgs) if error_msgs else None,
        now(),
    ))

    db.commit()
    db.close()

    print(f"\n✓ Seed complete in {elapsed:.2f}s")
    print(f"  Created : {created}")
    print(f"  Skipped : {skipped}")
    print(f"  Errors  : {errors}")
    print(f"  DB      : {DB_PATH}")

if __name__ == '__main__':
    run()
