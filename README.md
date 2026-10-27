# SatQuery AI – Backend (Prototype)

A FastAPI backend for **SatQuery AI**, a concept app that lets users ask natural-language questions about satellite images (e.g. *"Is there water in this area?"*) and see an answer with a highlighted region.

> ⚠️ **Prototype / demo:** this backend does **not** run a trained vision model yet. Answers come from simple keyword matching on the user's question, and the confidence scores and highlight regions are **simulated** (generated deterministically from a hash of the image and query). It exists to demonstrate the API design and the front-end experience.

## Features

- `POST /analyze`: upload one image plus a question and get an answer, a label, a simulated confidence, a highlight region and a processing trace
- `POST /change-analysis`: upload "before" and "after" images and get a simulated change score and region
- `GET /health`: health check
- CORS enabled for front-end use

Supported query themes: water, buildings/urban, vegetation/crops, roads.

## Tech stack

- Python, FastAPI, Uvicorn
- Pillow (reads image size)
- python-multipart (file uploads)

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to try the API in your browser.

## Example

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -F "query=Is there a lake in this image?" \
  -F "image=@sample.jpg"
```

## Roadmap

- [ ] Replace the simulated logic with a real vision-language model (e.g. CLIP or a remote-sensing VQA model)
- [ ] Real change detection using image differencing
- [ ] Add tests

## Author

Perarasu Boopathirajan M · Built with AI-assisted development
