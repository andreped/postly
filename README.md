---
title: 'Postly: a simple twitter clone'
colorFrom: indigo
colorTo: indigo
sdk: streamlit
sdk_version: '1.39.0'
python_version: '3.10'
app_port: 7860
emoji: 🫁
pinned: false
license: mit
app_file: app.py
---

# Postly

[![license](https://img.shields.io/github/license/DAVFoundation/captain-n3m0.svg?style=flat-square)](https://github.com/andreped/postly/blob/main/LICENSE.md)
<a target="_blank" href="https://huggingface.co/spaces/andreped/postly"><img src="https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-yellow.svg"></a>

This repository contain the Postly client, which serves as a micro-message communication platform, similar to Twitter.

To access the live demo, click on the `Hugging Face` badge above. Below is a snapshot of the current state of the demo app.

<img width="1400" alt="Screenshot" src="assets/streamlit-app-demo.png">

## Getting started

Install dependencies:
```
pip install -r requirements.txt
```

Run streamlit app:
```
streamlit run app.py
```

## Testing

For this project, we perform continuous integration to make sure that code is tested and formatted appropriately:

| Build Type | Status |
| - | - |
| **Unit tests** | [![CI](https://github.com/andreped/postly/workflows/Tests/badge.svg)](https://github.com/andreped/postly/actions) |
| **Check file size** | [![CI](https://github.com/andreped/postly/workflows/Check%20file%20size/badge.svg)](https://github.com/andreped/postly/actions) |
| **Unit tests** | [![CI](https://github.com/andreped/postly/workflows/Deploy/badge.svg)](https://github.com/andreped/postly/actions) |

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
