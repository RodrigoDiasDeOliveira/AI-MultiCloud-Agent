#!/usr/bin/env bash
set -euo pipefail
export APP_ENV=development
export APP_HOST=0.0.0.0
export APP_PORT=8000
exec uvicorn ai_multicloud_agent.main:app --host "$APP_HOST" --port "$APP_PORT" --reload
