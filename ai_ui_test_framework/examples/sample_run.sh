# #!/bin/bash
# set -e

# URL=$1
# MODEL=$2

# if [ -z "$URL" ] || [ -z "$MODEL" ]; then
#   echo "Usage: ./examples/sample_run.sh <url> <ollama_model>"
#   exit 1
# fi

# # Ensure venv exists
# if [ ! -d "venv" ]; then
#   echo "⚡ Creating virtual environment..."
#   python3 -m venv venv
# fi

# # Activate venv
# source venv/bin/activate

# # Ensure dependencies
# pip install --upgrade pip
# pip install -r requirements.txt
# pip install playwright
# playwright install

# echo "🚀 Running AI UI Test Framework"
# #python runner.py "$URL" "$MODEL"
# $(dirname "$0")/../venv/bin/python runner.py "$URL" "$MODEL"


#!/usr/bin/env bash
set -e
URL="$1"
MODEL="${2:-smollm2:135m}"

python - <<PY
from analyzer import run as analyze
from test_generator import generate_tests
from runner import run as run_tests
from report import make_report

an = analyze("${URL}")
print("Analyzed page:", an["title"], an["url"])
tests = generate_tests("${MODEL}", an)
print("Generated", len(tests), "tests")
results = run_tests(an["url"], tests)
make_report(results)
PY

