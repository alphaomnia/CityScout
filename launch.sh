#!/usr/bin/env bash
# CityScout launcher — kills any existing instances then starts both servers.

PROJECT="/home/alphaomnia/Projects/CityScout"
LOG="$PROJECT/backend/servers.log"

echo "=== CityScout Launch $(date) ===" >> "$LOG"

# ── Kill existing instances ───────────────────────────────────────────────
echo "Stopping existing servers..."
pkill -f "uvicorn main:app --port 8766" 2>/dev/null && echo "  Stopped uvicorn" >> "$LOG"
pkill -f "http.server 8080"             2>/dev/null && echo "  Stopped http.server" >> "$LOG"
sleep 1

# ── Start static file server ─────────────────────────────────────────────
cd "$PROJECT"
nohup python3 -m http.server 8080 >> "$LOG" 2>&1 &
echo "  http.server started (pid $!)" >> "$LOG"

# ── Start FastAPI backend ─────────────────────────────────────────────────
cd "$PROJECT/backend"
nohup uvicorn main:app --port 8766 >> "$LOG" 2>&1 &
echo "  uvicorn started (pid $!)" >> "$LOG"

sleep 2

# ── Open browser ──────────────────────────────────────────────────────────
xdg-open "http://localhost:8080/globe.html" >> "$LOG" 2>&1 &

echo "CityScout is running."
echo ""
echo "  Globe:  http://localhost:8080/globe.html"
echo "  API:    http://localhost:8766/health"
echo "  Logs:   $LOG"
echo ""
echo "This window will close in 5 seconds..."
sleep 5
