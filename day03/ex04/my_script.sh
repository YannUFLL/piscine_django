#!/bin/sh
set -e
python3 -m venv django_venv
. django_venv/bin/activate
pip install -r requirement.txt
exec $SHELL