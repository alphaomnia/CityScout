# CityScout — Claude Code Instructions

## Branch policy
- **Always commit and push directly to `main`.**
- Do NOT use feature branches unless the user explicitly requests one.
- GitHub Pages serves from `main`. Any change not on `main` is invisible to the user.
- After every batch of changes, verify with `git log --oneline origin/main` that commits are visible on `main`.

## Project overview
Multi-country restaurant aggregator for Europe. Static site hosted on GitHub Pages at `https://alphaomnia.github.io/CityScout/`.

## Key files
- `docs/restaurants.json` — central data store (restaurants, changelog, versioning)
- `docs/restaurants.html` — generated from `docs/_restaurants_template.html` on each workflow run
- `docs/dashboard.html` — analytics dashboard (static, hand-maintained)
- `restaurant_adapters/` — data source adapters (OpenStreetMap, FindSmiley only)
- `restaurants_config.yaml` — active cities and adapters
- `.github/workflows/daily_restaurants.yml` — daily aggregation workflow

## Active adapters
- `openstreetmap` — all 44 cities, no API key needed
- `findsmiley` — Denmark only (Copenhagen, Aarhus), free XML bulk download, adds hygiene scores

## Removed adapters (do not re-add without user approval)
- `foursquare` — free tier removed by Foursquare in 2024 (410 Gone)
- `here` — no API key available
- `google_places` — paid only, user explicitly declined
- `mapy_cz` — not functional

## Data notes
- `restaurants.json` source field may contain legacy `foursquare`/`here` values from old runs — harmless, those entries won't be updated
- `country`/`city` fields on Prague entries need a workflow run to backfill (trigger manually at github.com/alphaomnia/CityScout/actions)

## No Google Places API
User explicitly does not want Google Places API — it is paid. Do not suggest or add it.
