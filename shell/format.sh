#!/bin/bash
isort --sl postly/
black --line-length 120 .
flake8 --max-line-length 120 .
