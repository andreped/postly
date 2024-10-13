---
title: 'Postly: a simple twitter clone'
colorFrom: indigo
colorTo: indigo
sdk: streamlit
sdk_version: '1.13.0'
python_version: '3.10'
app_port: 7860
emoji: 🫁
pinned: false
license: mit
app_file: app.py
---

# Postly

This repository contain the Postly client, which serves as a micro-message communication platform, similar to Twitter.

## Getting started

Implemented client requires only Python >=3.7, no additional requirements.

To use client, simply do something like this:
```
from postly.clients import PostlyClient

postly_instance = PostlyClient()
```

## Testing

For this project, we perform continuous integration to make sure that code is tested and formatted appropriately:

| Build Type | Status |
| - | - |
| **Unit tests** | [![CI](https://github.com/andreped/postly/workflows/Tests/badge.svg)](https://github.com/andreped/postly/actions) |

To perform unit tests, you need to install `pytest`. For running formatting checks you also need `flake8`, `isort`, and `black`. We also depend on `pydantic` for type validation. To do so, lets configure a virtual environment:
```
python -m venv venv/
source venv/bin/activate

pip install -r requirements.txt
```

Then run this command to perform unit tests:
```
pytest -v tests/
```

To perform formatting checks, run the following:
```
sh shell/lint.sh
```

## License

This project has MIT license.
