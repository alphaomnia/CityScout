-- CityScout · Green 1 Schema
-- Six objects per Domain_B_Green_1_Build_Scope.md

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- ── 1. source ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS source (
    source_id         TEXT PRIMARY KEY,
    source_name       TEXT NOT NULL,
    source_type       TEXT NOT NULL,  -- saved_places|guidebook|screenshot|human_note|offline_photo|sheet|form
    coverage_city     TEXT,
    coverage_country  TEXT,
    coverage_region   TEXT,
    language          TEXT DEFAULT 'en',
    source_url_or_file TEXT,
    source_origin     TEXT NOT NULL,  -- web|guidebook|screenshot|human_note|offline_photo
    approval_status   TEXT NOT NULL DEFAULT 'proposed',  -- proposed|approved|rejected|needs_review
    quality_grade     TEXT NOT NULL DEFAULT 'unknown',   -- bronze|silver|gold|platinum|unknown
    why_this_grade    TEXT,
    known_bias        TEXT,
    created_at        TEXT NOT NULL DEFAULT (datetime('now')),
    last_checked_at   TEXT
);

-- ── 2. source_claim ────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS source_claim (
    claim_id               TEXT PRIMARY KEY,
    source_id              TEXT NOT NULL REFERENCES source(source_id),
    raw_place_name         TEXT NOT NULL,
    raw_excerpt_or_summary TEXT,
    raw_language           TEXT DEFAULT 'en',
    translated_summary     TEXT,
    city                   TEXT,
    country                TEXT,
    claimed_address        TEXT,
    claimed_reason_or_blurb TEXT,
    claimed_category_tags  TEXT,  -- JSON array
    source_confidence      REAL DEFAULT 0.5,
    parse_confidence       REAL DEFAULT 0.5,
    candidate_id           TEXT REFERENCES candidate(candidate_id),
    poi_match_status       TEXT DEFAULT 'unmatched',  -- matched|unmatched|ambiguous|rejected
    created_at             TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ── 3. candidate ───────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS candidate (
    candidate_id               TEXT PRIMARY KEY,
    canonical_name             TEXT NOT NULL,
    city                       TEXT NOT NULL,
    country                    TEXT NOT NULL,
    neighborhood               TEXT,
    google_place_id_or_url     TEXT,
    address                    TEXT,
    lat                        REAL,
    lng                        REAL,
    candidate_status           TEXT NOT NULL DEFAULT 'stub',
    -- stub|needs_match|source_backed|human_observed|needs_review|
    -- needs_visit|approved_for_inclusion|rejected|published
    inclusion_status           TEXT DEFAULT 'undecided',  -- include|exclude|undecided
    publish_status             TEXT DEFAULT 'not_ready',  -- not_ready|publish_ready|published
    source_count               INTEGER DEFAULT 0,
    verified_observation_count INTEGER DEFAULT 0,
    primary_source_id          TEXT REFERENCES source(source_id),
    confidence_summary         TEXT,
    needs_visit                INTEGER DEFAULT 0,
    needs_enrichment           INTEGER DEFAULT 0,
    created_from               TEXT DEFAULT 'manual',
    -- source|offline_source|saved_place|verified_review|manual|worker
    category                   TEXT,
    food_type                  TEXT,
    dining_type                TEXT,
    seating                    TEXT,
    description                TEXT,
    image_url                  TEXT,
    tags                       TEXT,  -- JSON array
    slug                       TEXT,
    tier                       TEXT,
    created_at                 TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at                 TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ── 4. observation ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS observation (
    observation_id       TEXT PRIMARY KEY,
    candidate_id         TEXT REFERENCES candidate(candidate_id),
    poi_reference        TEXT,
    place_name           TEXT NOT NULL,
    city                 TEXT,
    country              TEXT,
    reviewer             TEXT,
    date_visited         TEXT,
    visit_type           TEXT DEFAULT 'first_hand',
    -- first_hand|trusted_expert|scout|founder|soft_verification
    freeform_notes       TEXT,
    inclusion_signal     TEXT DEFAULT 'unsure',  -- include|exclude|unsure
    classification_signal TEXT DEFAULT 'unknown', -- good|great|exceptional|unknown
    why_include_or_exclude TEXT,
    price_signal         TEXT,
    value_signal         TEXT,
    good_for_signal      TEXT,
    vibe_signal          TEXT,
    confidence           REAL DEFAULT 0.7,
    created_at           TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ── 5. decision_log ────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS decision_log (
    decision_id        TEXT PRIMARY KEY,
    candidate_id       TEXT NOT NULL REFERENCES candidate(candidate_id),
    previous_status    TEXT,
    new_status         TEXT NOT NULL,
    decision_type      TEXT NOT NULL,
    -- candidate_created|dedupe|inclusion|rejection|needs_visit|publish|
    -- status_change|manual_override
    reason             TEXT NOT NULL,
    decider            TEXT NOT NULL DEFAULT 'system',
    evidence_reference TEXT,
    created_at         TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ── 6. job_run ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS job_run (
    job_run_id      TEXT PRIMARY KEY,
    worker_name     TEXT NOT NULL,
    input_type      TEXT,
    input_id        TEXT,
    batch_id        TEXT,
    status          TEXT NOT NULL DEFAULT 'success',
    -- success|warning|failed|blocked|partial
    severity        TEXT NOT NULL DEFAULT 'info',
    -- info|warning|high|critical
    created_count   INTEGER DEFAULT 0,
    updated_count   INTEGER DEFAULT 0,
    skipped_count   INTEGER DEFAULT 0,
    error_count     INTEGER DEFAULT 0,
    error_summary   TEXT,
    alert_created   INTEGER DEFAULT 0,
    retry_available INTEGER DEFAULT 0,
    resolved_status TEXT DEFAULT 'open',  -- open|resolved|ignored
    owner           TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    resolved_at     TEXT
);

-- ── Indexes ────────────────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_candidate_city    ON candidate(city);
CREATE INDEX IF NOT EXISTS idx_candidate_status  ON candidate(candidate_status);
CREATE INDEX IF NOT EXISTS idx_candidate_country ON candidate(country);
CREATE INDEX IF NOT EXISTS idx_claim_source      ON source_claim(source_id);
CREATE INDEX IF NOT EXISTS idx_claim_candidate   ON source_claim(candidate_id);
CREATE INDEX IF NOT EXISTS idx_obs_candidate     ON observation(candidate_id);
CREATE INDEX IF NOT EXISTS idx_decision_candidate ON decision_log(candidate_id);
CREATE INDEX IF NOT EXISTS idx_jobrun_status     ON job_run(status);
CREATE INDEX IF NOT EXISTS idx_jobrun_worker     ON job_run(worker_name);
