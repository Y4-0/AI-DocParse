# AI-DocParse

AI-powered document parser that converts PDFs and images into structured JSON using Vision Language Models.

## To be noted

Capable of using ollama Qwen2.5-VL or GPT-4o-mini which can be changed in line 12 of "main.py", ollama Qweb2.5-VL is set to local host i.e runs on model installed locally and would require you to change the url if you plan on not running it locally. NOTE THAT USING AI USING PARSE DOCUMENT COULD BE INACCURATE AT TIMES AND ITS RECOMENDED TO RECHECK THE OUTPUT. Results with GPT and could fail to load.

## Features

- PDF to image conversion
- Invoice parsing
- Delivery Challan parsing
- Local inference using Ollama
- OpenAI compatible
- Structured JSON output

## Tech Stack

- Python
- PyMuPDF
- OpenAI SDK
- Ollama
- Qwen2.5-VL

## Example Output

{
    "document_type": "...",
    "company_name": "...",
    "line_items": [...]
}

## HOW TO USE

Install the dependencies requirements via the installation process.
Insert the pdf into the parent forlder along with the main.py file.
execute/run 'main.py'.
The output will be generated and placed right beside the pdf placed orginally.

## Installation

pip install -r requirements.txt

## Run

python main.py