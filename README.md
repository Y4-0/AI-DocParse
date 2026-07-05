# AI-DocParse

AI-powered document parser that converts PDFs and images into structured JSON using Vision Language Models.
# USES OLLAMA Qwen2.5-VL OR GPT4o-mini WHICH CAN BE SWITCHED IN 12TH LINE OF main.py. NOTE THAT USING AI USING PARSE DOCUMENT COULD BE INACCURATE AT TIMES AND ITS RECOMENDED TO RECHECK THE OUTPUT

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

## HOW TO USE

Insert the pdf into the parent forlder along with the main.py file and execute/run main.py
The output will be generated and placed right beside the pdf placed orginally.

## Run

python main.py