import sys
import io
import os
import subprocess

from importlib.metadata import version
from PIL import Image

import requests
import gradio as gr


def r_version():
    return subprocess.run([r_bin_path, "--version"], capture_output=True, text=True)


def start_r_api(r_bin):
    command = [r_bin, "--no-save", "<", "start_api.R", "&"]

    print("Starting R API...")
    print(" ".join(command))

    os.system(" ".join(command))


# Config
concurrency_limit = 5
r_api_url = "http://localhost:8077"
r_bin_path = "/usr/bin/r"

examples = [
    """I begin this story with a neutral statement.  
Basically this is a very silly test.  
You are testing the Syuzhet package using short, inane sentences.  
I am actually very happy today. 
I have finally finished writing this package.  
Tomorrow I will be very sad. 
I won't have anything left to do. 
I might get angry and decide to do something horrible.  
I might destroy the entire package and start from scratch.  
Then again, I might find it satisfying to have completed my first R package. 
Honestly this use of the Fourier transformation is really quite elegant.  
You might even say it's beautiful!""",
]

title = "R with Gradio"

# https://www.tablesgenerator.com/markdown_tables
authors_table = """
## Authors

Follow them on social networks and **contact** if you need any help or have any questions:

| <img src="https://avatars.githubusercontent.com/u/7875085?v=4" width="100"> **Yehor Smoliakov** |
|-------------------------------------------------------------------------------------------------|
| https://t.me/smlkw in Telegram                                                                  |
| https://x.com/yehor_smoliakov at X                                                              |
| https://github.com/egorsmkv at GitHub                                                           |
| https://huggingface.co/Yehor at Hugging Face                                                    |
| or use egorsmkv@gmail.com                                                                       |
""".strip()

description_head = f"""
# {title}

## Overview

This is a demo for R with Gradio app that uses https://github.com/mjockers/syuzhet
""".strip()

description_foot = f"""
{authors_table}
""".strip()

tech_env = f"""
#### Environment

- Python: {sys.version}
""".strip()

r_version_info = r_version()
if r_version_info.returncode != 0:
    print("Error: R version command failed.")
    exit(1)
r_tech_env = f"""
#### R Environment

```
{r_version_info.stdout.strip()}
```
""".strip()

tech_libraries = f"""
#### Libraries

- requests: {version('requests')}
- gradio: {version('gradio')}
""".strip()


def call_api(text):
    url = r_api_url + "/sentiment-plot"
    data = {"text": text}

    response = requests.post(url, data=data)

    if response.status_code != 200:
        return None

    return response


def inference(text, progress=gr.Progress()):
    if not text:
        raise gr.Error("Please paste your text.")

    gr.Info("Calling the R API", duration=2)

    progress(0, desc="Working...")

    response = call_api(text)

    if not response:
        image = "-"
    else:
        # Save the image to a file
        # with open("plot.png", "wb") as f:
        #     f.write(response.content)

        image = Image.open(io.BytesIO(response.content))

    gr.Info("Finished!", duration=2)

    return image


demo = gr.Blocks(
    title=title,
    analytics_enabled=False,
    theme="huggingface",
    # theme=gr.themes.Base(),
)

with demo:
    gr.Markdown(description_head)

    gr.Markdown("## Usage")

    with gr.Row():
        text = gr.Textbox(label="Text", autofocus=True, max_lines=50)

        sentiment_plot = gr.Image(
            label="Sentiment plot",
        )

    gr.Button("Analyze").click(
        inference,
        concurrency_limit=concurrency_limit,
        inputs=text,
        outputs=sentiment_plot,
    )

    with gr.Row():
        gr.Examples(label="Choose an example", inputs=text, examples=examples)

    gr.Markdown(description_foot)

    gr.Markdown("### Gradio app uses:")
    gr.Markdown(tech_env)
    gr.Markdown(r_tech_env)
    gr.Markdown(tech_libraries)

if __name__ == "__main__":
    start_r_api(r_bin_path)

    demo.queue()
    demo.launch()
