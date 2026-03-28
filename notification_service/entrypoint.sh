#!/bin/bash
# entrypoint.sh

echo "🚀 Starting server..."
uvicorn main:app --host 0.0.0.0 --port 8080 --reload