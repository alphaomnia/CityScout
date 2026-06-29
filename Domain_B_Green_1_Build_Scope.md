# Domain B · Green 1 Build Scope
### The ingestion substrate and candidate universe engine
*Source of truth: Andrew's "B - System Workflow" and "B - Research Agenda" briefs, plus the City Build Workflow V1 diagram. Anything added that is not stated in those is marked **[ASSUMPTION]** for you and Andrew to confirm or overrule before it hardens.*

---

## 0. What this is, and what it is not

This is the build scope for the **Green 1s**: the minimum objects, workers, and surfaces needed to start manufacturing a real candidate universe. It is the engine behind the candidate lifecycle, nothing downstream of it.

**Build target.** A system that can take Andrew's existing corpus (saved Google places, guidebooks, screenshots, forms, sheets, travel notes, verified observations) and turn it into structured source records, source claims, verified observations, and candidate place records, then let a human review the candidate universe by city and status.

**Explicitly not in this build.** Scoring, final inclusion rules, taxonomy, personalisation, menus, photo strategy, production-grade enrichment, publish-ready place pages. Those are B3 to B8 and are deferred. If the build starts reaching into them, that is the signal to stop and cut back.

The test this build must pass: can we go from roughly 100 places today to **hundreds or thousands of structured candidates across several ecosystems**, most of them incomplete, fast enough to make a multi-city plan plausible to study.

**[ASSUMPTION] Stack.** The system briefs assume Lovable. You have said you are building the aggregator directly in Claude Code. This scope is written tool-agnostic on the data model and workers, which suit a Claude Code build. The human review surfaces (section 4) can be a thin local UI for Green 1 and move to Lovable later if that proves better. Confirm the split you want.

---

## 1. The six objects (data foundation)

Build these first. Everything else depends on them. Keep candidate records and official records cleanly separable from day one, even if you start with one table plus a status.

| Object | Purpose |
|---|---|
| `source` | Registry of sources, graded and approved, with provenance. |
| `source_claim` | What a source said about a place. The evidence layer. Never becomes published copy. |
| `candidate` | The working universe of possible places. Supports incomplete stubs. |
| `observation` | First-hand or trusted human reviews. Highest-trust input. Can create or update a candidate. |
| `decision_log` | Every status change and decision, with reason and decider. Preserves the why. |
| `job_run` | Every worker run and its outcome. Prevents silent ingestion failure. |

### Minimal schemas (key fields only)

**source** — `source_id`, `source_name`, `source_type`, `coverage_city/country/region`, `language`, `source_url_or_file`, `source_origin` (web / guidebook / screenshot / human_note / offline_photo), `approval_status` (proposed / approved / rejected / needs_review), `quality_grade` (bronze / silver / gold / platinum / unknown), `why_this_grade`, `known_bias`, `created_at`, `last_checked_at`.
> Rule: a source can be stored before approval, but an unapproved source must not auto-mine candidates without review.

**source_claim** — `claim_id`, `source_id`, `raw_place_name`, `raw_excerpt_or_summary`, `raw_language`, `translated_summary`, `city/country`, `claimed_address`, `claimed_reason_or_blurb`, `claimed_category_tags`, `source_confidence`, `parse_confidence`, `candidate_id` (if matched), `poi_match_status`, `created_at`.

**candidate** — `candidate_id`, `canonical_name`, `city`, `country`, `neighborhood`, `google_place_id_or_url`, `address`, `lat`, `lng`, `candidate_status`, `inclusion_status`, `publish_status`, `source_count`, `verified_observation_count`, `primary_source_id`, `confidence_summary`, `needs_visit`, `needs_enrichment`, `created_from` (source / offline_source / saved_place / verified_review / manual / worker), `created_at`, `updated_at`.

**observation** — `observation_id`, `candidate_id` (if matched), `poi_reference`, `place_name`, `city/country`, `reviewer`, `date_visited`, `visit_type` (first_hand / trusted_expert / scout / founder / soft_verification), `freeform_notes`, `inclusion_signal` (include / exclude / unsure), `classification_signal` (good / great / exceptional / unknown), `why_include_or_exclude`, `price_signal`, `value_signal`, `good_for_signal`, `vibe_signal`, `confidence`, `created_at`.

**decision_log** — `decision_id`, `candidate_id`, `previous_status`, `new_status`, `decision_type` (candidate_created / dedupe / inclusion / rejection / needs_visit / publish / status_change / manual_override), `reason`, `decider`, `evidence_reference`, `created_at`.

**job_run** — `job_run_id`, `worker_name`, `input_type`, `input_id`, `batch_id`, `status` (success / warning / failed / blocked / partial), `severity` (info / warning / high / critical), `created_count`, `updated_count`, `skipped_count`, `error_count`, `error_summary`, `alert_created`, `retry_available`, `resolved_status` (open / resolved / ignored), `owner`, `created_at`, `resolved_at`.

---

## 2. Candidate lifecycle (statuses)

Every candidate has an explicit state. The near-term build need not complete the whole lifecycle, but must not create records that cannot later move through it.

```
source / observation / import found
  -> parsed
  -> POI matched or needs_match
  -> stub created
  -> source_backed or human_observed
  -> needs_review
  -> approved_for_inclusion / rejected / needs_visit
  -> machine_enriched
  -> publish_ready or needs_publish_completion
  -> published
```

**Minimum statuses for Green 1:** `stub`, `needs_match`, `source_backed`, `human_observed`, `needs_review`, `needs_visit`, `approved_for_inclusion`, `rejected`, `published`.

Two decisions stay separate throughout, because they are the hinge of the whole December question:
- **Include** = this place belongs in the guide.
- **Publish** = this place is ready to appear to users.

A place can be approved for inclusion and still not be publish-ready (no photos, blurb, price confidence, hours, or QA). Green 1 builds toward Include. Publish is measured separately (see section 7).

---

## 3. Intake workers

Each worker takes an input, produces records, and must end in one logged outcome: success / success_with_warnings / partial_success / blocked / failed. No worker fails silently.

| Worker | Input | Output |
|---|---|---|
| Existing corpus import | Google saved places, guidebooks, sheets, forms, notes | Source records, observations, candidate stubs |
| Offline source parser | Screenshots, magazine photos, offline images | Parsed source claims, possible POI candidates |
| Source parser | Approved source material | Source claims and candidate leads |
| Candidate stub creator | Source claim, saved place, observation, POI | Candidate record |
| POI match / place fundamentals | Candidate lead, POI, Google URL, name, address | Deduped canonical candidate |
| Verified review to candidate | Human observation | New candidate or candidate update |
| Language / translation helper | Non-English source text | Stored original plus translated interpretation |
| Batch import monitor | Large imports | Run summary: created / skipped / error counts |

**[ASSUMPTION]** First worker to build is **existing corpus import**, because Andrew's saved Google places and sheets are the fastest path to volume. Offline parser and source parser follow. Confirm the order.

---

## 4. Human surfaces (thin for Green 1)

| Surface | Purpose | Green 1 weight |
|---|---|---|
| Verified review form | Log real observations straight into the system | Build properly. This is the highest-trust input. |
| Candidate universe view / map | See candidates by city, status, density, gaps, source | Build properly. This is where you study the city. |
| Candidate review queue | Bite-sized accept / reject / needs-visit decisions with reasons | Build properly. |
| Needs-visit backlog | Places awaiting human verification | Light. |
| Alert / failure inbox | Failed imports, low-confidence matches, parser errors | Light, but present. |
| Basic publish view | Evidence chain and status before approval | Lightest. Stub only for Green 1. |

The first build should be a usable ingestion and review substrate, not a polished internal admin product.

---

## 5. Alerts and failure surfaces

Failures route to a queue, never to nowhere. Severity drives attention.

| Severity | Meaning |
|---|---|
| Info | Useful result, no action. |
| Warning | Record usable but low-confidence or incomplete. |
| High | Human action needed before the candidate proceeds. |
| Critical | Pipeline or data-integrity issue. |

Alert types to wire from the start: source not approved, parse failed, OCR readability low, translation low-confidence, POI match ambiguous, duplicate candidate risk, missing critical fields, batch partial failure, worker created zero candidates, claims unlinked to a candidate, candidate stuck in status, decision missing a reason, publish attempted before readiness, external source unavailable.

---

## 6. Instrumentation from day one (non-negotiable)

This is the part that turns the December deadline from a guess into arithmetic. Capture these on every run and every city, from the first import:

- processing time per source and per batch
- source yield (candidates per source)
- source overlap (unique vs duplicated candidates across sources)
- extraction / parse error rate
- POI match success rate
- duplicate rate
- human review time per task
- candidate count per ecosystem
- confidence flags and needs-verification count

Without this, you finish Green 1 with a dataset but no cost numbers, and the footprint decision stays a guess. With it, the per-city candidate-universe cost falls out of the logs directly.

---

## 7. The publish-readiness probe (added on purpose)

Andrew's agenda stops Green 1 at the candidate universe. The December commitment needs the Include-to-Publish cost, which the agenda defers. So run one deliberate, isolated probe: take a single ecosystem all the way to publish-ready and time every step.

**[ASSUMPTION]** Use **Prague** for the probe, because the trust path is strongest there, so you measure publish cost without foreign-market noise confounding it. Malta is the better choice for the separate local-reaction test. Confirm.

Output: the founder-hours to move one city from approved_for_inclusion to publish_ready, broken down by enrichment, verification, and QA. Multiplied across harder cities, this is the first real read on whether seven by December is reachable.

---

## 8. Build order

1. The six objects and their schema. Candidate and official records separable.
2. Instrumentation layer (`job_run`, `decision_log`, the metrics in section 6). Build it before the workers so nothing runs uninstrumented.
3. Existing corpus import worker plus batch import monitor.
4. POI match / place fundamentals and candidate stub creator (with dedupe flags).
5. Verified review form and the candidate universe view / map.
6. Candidate review queue with reasons, plus needs-visit backlog.
7. Offline source parser and source parser.
8. Alert / failure inbox.
9. Dry run: import one real batch end to end, confirm candidates, provenance, dedupe flags, and the metrics all export cleanly per city.

---

## 9. Guardrails to preserve (do not let these blur)

- Candidate DB vs Official DB.
- Source evidence vs published copy (never copy source language into product text).
- Worker (gathers, extracts, drafts) vs Engine (judges, scores, prioritises). Green 1 is almost all workers.
- Machine structures; human judges, approves, rejects, sets the bar.
- Every candidate links to its provenance. Every rejection keeps its why-not.

---

## 10. Open founder decisions (raise before or during build)

| ID | Decision | Owner |
|---|---|---|
| B1 | Candidate and Official: one table with statuses, or separate tables? If separate, which fields overlap? | Reuben + Claude |
| B2 | Is Google Place ID the primary identity anchor? How are venues without a clear listing handled? How are chains and branches handled? | Reuben + Claude |
| B3 | Can unapproved sources create candidates, or only propose them? How do quality grades work initially? | Andrew |
| B4 | Verified review form: structured, freeform, or hybrid? Which fields are mandatory? Can a review auto-create a candidate? | Andrew + Reuben |
| B5 | What is the minimum candidate stub, and the minimum official published record? | Andrew + Reuben |
| B6 | How much POI ambiguity triggers manual review? Do import batches require review before candidates are created? | Reuben + Claude |
| B7 | Which ecosystem takes the publish-readiness probe (section 7)? | Reuben + Claude |

---

## 11. Success criteria

Green 1 succeeds if you can: ingest a batch of saved places, ingest a batch of source-derived places, capture verified reviews directly, auto-create candidate stubs, flag likely duplicates, see candidates on a map by city / status / source, review candidates in a queue, reject with reasons, send to needs-visit, preserve provenance, see failed and partial runs, and read where ingestion is breaking.

It is **not** judged on whether candidates are enriched, scored, tagged, or publish-ready. It is judged on whether it creates a real working dataset large enough to pressure-test city manufacturing, with the cost of doing so visible in the logs.
