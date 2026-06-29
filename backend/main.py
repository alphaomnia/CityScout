"""
CityScout · Green 1 API
FastAPI backend — all six objects, candidate lifecycle, instrumentation.
Run: uvicorn main:app --reload --port 8765
"""
import json, sqlite3, uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DB_PATH = Path(__file__).parent / "cityscout.db"

app = FastAPI(title="CityScout Green 1", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── DB helpers ──────────────────────────────────────────────────────────────

def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    return db

def now():
    return datetime.now(timezone.utc).isoformat()

def row_to_dict(row):
    if row is None:
        return None
    d = dict(row)
    for k, v in d.items():
        if isinstance(v, str) and v.startswith('['):
            try: d[k] = json.loads(v)
            except Exception: pass
    return d

# ── Pydantic models ─────────────────────────────────────────────────────────

class CandidateCreate(BaseModel):
    canonical_name:   str
    city:             str
    country:          str
    neighborhood:     Optional[str] = None
    address:          Optional[str] = None
    lat:              Optional[float] = None
    lng:              Optional[float] = None
    category:         Optional[str] = None
    description:      Optional[str] = None
    created_from:     str = "manual"
    primary_source_id: Optional[str] = None
    google_place_id_or_url: Optional[str] = None

class CandidateStatusUpdate(BaseModel):
    new_status:    str
    reason:        str
    decider:       str = "founder"
    decision_type: str = "status_change"

class ObservationCreate(BaseModel):
    place_name:            str
    city:                  str = "Prague"
    country:               str = "Czech Republic"
    candidate_id:          Optional[str] = None
    reviewer:              Optional[str] = None
    date_visited:          Optional[str] = None
    visit_type:            str = "first_hand"
    freeform_notes:        Optional[str] = None
    inclusion_signal:      str = "unsure"
    classification_signal: str = "unknown"
    why_include_or_exclude: Optional[str] = None
    price_signal:          Optional[str] = None
    value_signal:          Optional[str] = None
    good_for_signal:       Optional[str] = None
    vibe_signal:           Optional[str] = None
    confidence:            float = 0.7

class SourceCreate(BaseModel):
    source_name:    str
    source_type:    str
    source_origin:  str
    coverage_city:  Optional[str] = None
    coverage_country: Optional[str] = None
    language:       str = "en"
    source_url_or_file: Optional[str] = None
    quality_grade:  str = "unknown"
    why_this_grade: Optional[str] = None
    known_bias:     Optional[str] = None

# ── Health ──────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    db = get_db()
    counts = {
        "candidates": db.execute("SELECT COUNT(*) FROM candidate").fetchone()[0],
        "sources":    db.execute("SELECT COUNT(*) FROM source").fetchone()[0],
        "job_runs":   db.execute("SELECT COUNT(*) FROM job_run").fetchone()[0],
    }
    db.close()
    return {"status": "ok", "counts": counts}

# ── Stats / instrumentation ─────────────────────────────────────────────────

@app.get("/stats")
def stats(city: Optional[str] = None):
    db = get_db()
    where = "WHERE city=?" if city else ""
    params = (city,) if city else ()

    by_status = {
        row["candidate_status"]: row["n"]
        for row in db.execute(
            f"SELECT candidate_status, COUNT(*) as n FROM candidate {where} GROUP BY candidate_status",
            params
        )
    }
    by_city = {
        row["city"]: row["n"]
        for row in db.execute(
            "SELECT city, COUNT(*) as n FROM candidate GROUP BY city ORDER BY n DESC"
        )
    }
    source_yield = {
        row["source_name"]: row["n"]
        for row in db.execute("""
            SELECT s.source_name, COUNT(sc.claim_id) as n
            FROM source s LEFT JOIN source_claim sc ON s.source_id=sc.source_id
            GROUP BY s.source_id
        """)
    }
    job_summary = {
        row["status"]: row["n"]
        for row in db.execute("SELECT status, COUNT(*) as n FROM job_run GROUP BY status")
    }
    db.close()
    return {
        "by_status":    by_status,
        "by_city":      by_city,
        "source_yield": source_yield,
        "job_summary":  job_summary,
        "total_candidates": sum(by_status.values()),
    }

# ── Candidates ──────────────────────────────────────────────────────────────

VALID_STATUSES = {
    "stub", "needs_match", "source_backed", "human_observed",
    "needs_review", "needs_visit", "approved_for_inclusion",
    "rejected", "published",
}

@app.get("/candidates")
def list_candidates(
    city:    Optional[str] = None,
    status:  Optional[str] = None,
    country: Optional[str] = None,
    limit:   int = Query(500, le=2000),
    offset:  int = 0,
    search:  Optional[str] = None,
):
    db = get_db()
    clauses, params = [], []
    if city:    clauses.append("city=?");    params.append(city)
    if status:  clauses.append("candidate_status=?"); params.append(status)
    if country: clauses.append("country=?"); params.append(country)
    if search:  clauses.append("canonical_name LIKE ?"); params.append(f"%{search}%")
    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    rows = db.execute(
        f"SELECT * FROM candidate {where} ORDER BY canonical_name LIMIT ? OFFSET ?",
        params + [limit, offset]
    ).fetchall()
    total = db.execute(f"SELECT COUNT(*) FROM candidate {where}", params).fetchone()[0]
    db.close()
    return {"total": total, "items": [row_to_dict(r) for r in rows]}

@app.get("/candidates/{candidate_id}")
def get_candidate(candidate_id: str):
    db = get_db()
    row = db.execute("SELECT * FROM candidate WHERE candidate_id=?", (candidate_id,)).fetchone()
    if not row:
        raise HTTPException(404, "Candidate not found")
    cand = row_to_dict(row)
    cand["decisions"] = [row_to_dict(r) for r in db.execute(
        "SELECT * FROM decision_log WHERE candidate_id=? ORDER BY created_at DESC",
        (candidate_id,)
    ).fetchall()]
    cand["observations"] = [row_to_dict(r) for r in db.execute(
        "SELECT * FROM observation WHERE candidate_id=? ORDER BY created_at DESC",
        (candidate_id,)
    ).fetchall()]
    db.close()
    return cand

@app.post("/candidates", status_code=201)
def create_candidate(body: CandidateCreate):
    db = get_db()
    # Dedupe check
    existing = db.execute(
        "SELECT candidate_id FROM candidate WHERE canonical_name=? AND city=?",
        (body.canonical_name, body.city)
    ).fetchone()
    if existing:
        db.close()
        raise HTTPException(409, f"Candidate already exists: {existing['candidate_id']}")

    cid = str(uuid.uuid4())
    db.execute("""
        INSERT INTO candidate
          (candidate_id, canonical_name, city, country, neighborhood,
           address, lat, lng, candidate_status, created_from,
           primary_source_id, category, description,
           google_place_id_or_url, created_at, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        cid, body.canonical_name, body.city, body.country,
        body.neighborhood, body.address, body.lat, body.lng,
        "stub", body.created_from, body.primary_source_id,
        body.category, body.description, body.google_place_id_or_url,
        now(), now(),
    ))
    db.execute("""
        INSERT INTO decision_log
          (decision_id, candidate_id, previous_status, new_status,
           decision_type, reason, decider, created_at)
        VALUES (?,?,?,?,?,?,?,?)
    """, (
        str(uuid.uuid4()), cid, None, "stub",
        "candidate_created", f"Manual stub: {body.canonical_name}",
        "founder", now(),
    ))
    db.commit()
    row = db.execute("SELECT * FROM candidate WHERE candidate_id=?", (cid,)).fetchone()
    db.close()
    return row_to_dict(row)

@app.patch("/candidates/{candidate_id}/status")
def update_candidate_status(candidate_id: str, body: CandidateStatusUpdate):
    if body.new_status not in VALID_STATUSES:
        raise HTTPException(400, f"Invalid status: {body.new_status}")
    db = get_db()
    row = db.execute("SELECT * FROM candidate WHERE candidate_id=?", (candidate_id,)).fetchone()
    if not row:
        raise HTTPException(404, "Candidate not found")
    prev = row["candidate_status"]
    ts = now()

    # Derive inclusion/publish from new status
    incl = "include" if body.new_status == "approved_for_inclusion" else (
           "exclude" if body.new_status == "rejected" else row["inclusion_status"])
    pub  = "published" if body.new_status == "published" else (
           "publish_ready" if body.new_status == "approved_for_inclusion" else row["publish_status"])

    db.execute("""
        UPDATE candidate
        SET candidate_status=?, inclusion_status=?, publish_status=?,
            needs_visit=?, updated_at=?
        WHERE candidate_id=?
    """, (
        body.new_status, incl, pub,
        1 if body.new_status == "needs_visit" else row["needs_visit"],
        ts, candidate_id,
    ))
    db.execute("""
        INSERT INTO decision_log
          (decision_id, candidate_id, previous_status, new_status,
           decision_type, reason, decider, created_at)
        VALUES (?,?,?,?,?,?,?,?)
    """, (
        str(uuid.uuid4()), candidate_id, prev, body.new_status,
        body.decision_type, body.reason, body.decider, ts,
    ))
    db.commit()
    updated = row_to_dict(db.execute("SELECT * FROM candidate WHERE candidate_id=?", (candidate_id,)).fetchone())
    db.close()
    return updated

# ── Observations ────────────────────────────────────────────────────────────

@app.post("/observations", status_code=201)
def create_observation(body: ObservationCreate):
    db = get_db()
    oid = str(uuid.uuid4())
    db.execute("""
        INSERT INTO observation
          (observation_id, candidate_id, place_name, city, country,
           reviewer, date_visited, visit_type, freeform_notes,
           inclusion_signal, classification_signal, why_include_or_exclude,
           price_signal, value_signal, good_for_signal, vibe_signal,
           confidence, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        oid, body.candidate_id, body.place_name, body.city, body.country,
        body.reviewer, body.date_visited, body.visit_type, body.freeform_notes,
        body.inclusion_signal, body.classification_signal,
        body.why_include_or_exclude, body.price_signal, body.value_signal,
        body.good_for_signal, body.vibe_signal, body.confidence, now(),
    ))
    # If linked to a candidate, bump count and optionally advance status
    if body.candidate_id:
        db.execute("""
            UPDATE candidate
            SET verified_observation_count = verified_observation_count + 1,
                candidate_status = CASE
                    WHEN candidate_status='stub' THEN 'human_observed'
                    WHEN candidate_status='source_backed' THEN 'human_observed'
                    ELSE candidate_status
                END,
                updated_at=?
            WHERE candidate_id=?
        """, (now(), body.candidate_id))
        if body.inclusion_signal in ('include', 'exclude'):
            db.execute("""
                INSERT INTO decision_log
                  (decision_id, candidate_id, previous_status, new_status,
                   decision_type, reason, decider, created_at)
                VALUES (?,?,?,?,?,?,?,?)
            """, (
                str(uuid.uuid4()), body.candidate_id,
                None, "human_observed",
                "inclusion",
                f"Observation: {body.inclusion_signal} — {body.why_include_or_exclude or body.freeform_notes or ''}",
                body.reviewer or "founder", now(),
            ))
    db.commit()
    row = db.execute("SELECT * FROM observation WHERE observation_id=?", (oid,)).fetchone()
    db.close()
    return row_to_dict(row)

@app.get("/observations")
def list_observations(candidate_id: Optional[str] = None, city: Optional[str] = None):
    db = get_db()
    clauses, params = [], []
    if candidate_id: clauses.append("candidate_id=?"); params.append(candidate_id)
    if city:         clauses.append("city=?");         params.append(city)
    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    rows = db.execute(
        f"SELECT * FROM observation {where} ORDER BY created_at DESC", params
    ).fetchall()
    db.close()
    return [row_to_dict(r) for r in rows]

# ── Sources ─────────────────────────────────────────────────────────────────

@app.get("/sources")
def list_sources():
    db = get_db()
    rows = db.execute("SELECT * FROM source ORDER BY created_at DESC").fetchall()
    db.close()
    return [row_to_dict(r) for r in rows]

@app.post("/sources", status_code=201)
def create_source(body: SourceCreate):
    db = get_db()
    sid = str(uuid.uuid4())
    db.execute("""
        INSERT INTO source
          (source_id, source_name, source_type, coverage_city, coverage_country,
           language, source_url_or_file, source_origin, approval_status,
           quality_grade, why_this_grade, known_bias, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        sid, body.source_name, body.source_type,
        body.coverage_city, body.coverage_country, body.language,
        body.source_url_or_file, body.source_origin, "proposed",
        body.quality_grade, body.why_this_grade, body.known_bias, now(),
    ))
    db.commit()
    row = db.execute("SELECT * FROM source WHERE source_id=?", (sid,)).fetchone()
    db.close()
    return row_to_dict(row)

# ── Job runs ────────────────────────────────────────────────────────────────

@app.get("/job_runs")
def list_job_runs(status: Optional[str] = None, limit: int = 50):
    db = get_db()
    where = "WHERE status=?" if status else ""
    params = (status,) if status else ()
    rows = db.execute(
        f"SELECT * FROM job_run {where} ORDER BY created_at DESC LIMIT ?",
        params + (limit,)
    ).fetchall()
    db.close()
    return [row_to_dict(r) for r in rows]

@app.get("/alerts")
def list_alerts():
    db = get_db()
    rows = db.execute("""
        SELECT * FROM job_run
        WHERE (status IN ('failed','partial','blocked','warning')
               OR severity IN ('high','critical'))
          AND resolved_status='open'
        ORDER BY created_at DESC
    """).fetchall()
    db.close()
    return [row_to_dict(r) for r in rows]

@app.patch("/job_runs/{job_run_id}/resolve")
def resolve_job_run(job_run_id: str, resolved_status: str = "resolved"):
    db = get_db()
    db.execute(
        "UPDATE job_run SET resolved_status=?, resolved_at=? WHERE job_run_id=?",
        (resolved_status, now(), job_run_id)
    )
    db.commit()
    db.close()
    return {"ok": True}

# ── Decision log ────────────────────────────────────────────────────────────

@app.get("/decisions")
def list_decisions(candidate_id: Optional[str] = None, limit: int = 100):
    db = get_db()
    where = "WHERE candidate_id=?" if candidate_id else ""
    params = (candidate_id,) if candidate_id else ()
    rows = db.execute(
        f"SELECT * FROM decision_log {where} ORDER BY created_at DESC LIMIT ?",
        params + (limit,)
    ).fetchall()
    db.close()
    return [row_to_dict(r) for r in rows]
