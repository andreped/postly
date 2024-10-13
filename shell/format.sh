#!/bin/bash
isort --sl postly/ tests/ app.py
black --line-length 120 postly/ tests/ app.py
flake8 --max-line-length 120 postly/ tests/ app.py
