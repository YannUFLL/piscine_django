#!/bin/bash
set -e
python3 -m venv djangoenv
source djangoenv/bin/activate
pip install -r requirements.txt
$SHELL