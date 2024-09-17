# R with Gradio

This repository contains a simple example of using R with Gradio.

Idea:

- Start an HTTP API server in R using the `plumber` package.
- Call the API from Python using the `requests` package.

## Installation

Install R packages:

```
Rscript install_packages.R
```

Install Python packages:

```
uv venv --python 3.12

source .venv/bin/activate

uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt
```

## Run

Run R server (for example):

```
Rscript start_api.R
```

Run Gradio app with automatically starting the R server (in fork mode):

```
python app.py
```

## Production

Build the Docker image:

```
docker build -t r-with-gradio .
```
