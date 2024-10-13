#!/bin/bash
isort --sl postly/ app.py
black --line-length 120 postly/ app.py
flake8 --max-line-length 120 postly/ app.py
