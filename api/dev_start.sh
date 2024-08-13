#! /usr/bin/env sh

#. /app/prestart.sh

uvicorn src.main:app --reload --host 0.0.0.0 --port 8000