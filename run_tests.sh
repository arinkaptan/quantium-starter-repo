#!/bin/bash
set -e

if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: virtual environment 'venv' not found."
    exit 1
fi

pytest test_app.py --headless

exit 0