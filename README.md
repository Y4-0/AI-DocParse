# AI-DocParse

AI-powered document parser that converts PDFs and images into structured JSON using Vision Language Models.

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

## Installation

pip install -r requirements.txt

## Run

python main.py