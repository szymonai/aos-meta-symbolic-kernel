---
title: AOS Public Sandbox
sdk: gradio
app_file: app.py
license: other
---

# AOS Public Sandbox

This is a synthetic Gradio sandbox for the public AOS demonstrator. It exposes
bounded public demo logic only.

It does not publish private policies, production adapters, domain data,
deployment configuration, credentials, or persistence backends.

## Local Run

```bash
python -m pip install -r examples/gradio-sandbox/requirements.txt
python examples/gradio-sandbox/app.py
```

The same directory can be used as a Hugging Face Space with the Gradio SDK.
