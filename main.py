import base64
import json
import os
from typing import List
import fitz  # PyMuPDF
import openai
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

#choose what to use, either openai or ollama
USE_OLLAMA = True
if USE_OLLAMA:
    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )
    model = "qwen2.5vl:7b"
else:
    KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=KEY)
    model = "gpt-4o-mini"
    if not KEY:
        raise ValueError("OPENAI_API_KEY not found in environment variables. Please check pass.env")

# Load environment variables from pass.env (if available)
try:
    load_dotenv(dotenv_path="pass.env")
except ImportError:
    print("Warning: dotenv package not found. Environment variables must be set in shell.")

project_folder = Path(__file__).parent
supported_files = [".pdf", ".png", ".jpg", ".jpeg"]
for file in project_folder.iterdir():
    if file.suffix.lower() in supported_files:
        PATH = str(file)
        break
else:
    raise FileNotFoundError("No supported PDF or image found.")
if not PATH:
    raise ValueError("Path to input file ('path') not found in environment variables. Please check pass.env")
if not os.path.exists(PATH):
    raise FileNotFoundError(f'Input file does not exist: {PATH}')

def pdf_to_images(pdf_path: str) -> List[bytes]:
    """Convert a PDF file to a list of PNG image bytes using PyMuPDF."""
    doc = fitz.open(pdf_path)
    image_bytes_list = []
    for page in doc:
        pix = page.get_pixmap()
        image_bytes = pix.tobytes("png")
        image_bytes_list.append(image_bytes)
    return image_bytes_list

def read_image_bytes(image_path: str) -> bytes:
    """Read a standard image file and return its bytes."""
    with open(image_path, "rb") as f:
        return f.read()

def encode_image_base64(image_bytes: bytes) -> str:
    """Encode image bytes to base64 string."""
    return base64.b64encode(image_bytes).decode("utf-8")

def extract_info_from_images(image_bytes_list: List[bytes]) -> str:
    client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
    )
    """Send document images to OpenAI to extract structured JSON data."""
    
    content: List[dict] = [
        {
            "type": "text",
            "text": (
                "Please extract all relevant information from the attached document. "
                "Output the result as a raw JSON object containing the document metadata "
                "(document type, number, dates, company names, state, GSTIN/tax IDs), "
                "the list of line items (description, model, make, units, quantity, etc.), "
                "and any other notable information like receipt stamps, signatures, or total quantities."
            )
        }
    ]
    
    for img_bytes in image_bytes_list:
        base64_str = encode_image_base64(img_bytes)
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_str}"
            }
        })
        
    response = client.chat.completions.create(
        model="qwen2.5vl:7b",
        messages=[
            {
                "role": "system",
                "content": (
                    '''You are an expert document parser. Your goal is to analyze the document images 
                    provided and extract their information into structured JSON. Always respond with 
                    valid JSON only.'''
                )
            },
            {
                "role": "user",
                "content": content
            }
        ],
        temperature=0.0
    )
    
    return response.choices[0].message.content

def main():
    ext = os.path.splitext(PATH)[1].lower()
    
    print(f"Processing input file: {PATH}")
    
    image_bytes_list = []
    if ext == ".pdf":
        image_bytes_list = pdf_to_images(PATH)
    elif ext in [".jpeg", ".png", ".jpg"]:
        image_bytes_list = [read_image_bytes(PATH)]
    else:
        raise ValueError(f"Unsupported file extension: {ext}. Must be a PDF or image (JPEG, PNG, JPG).")
    
    if not image_bytes_list:
        raise ValueError("No pages/images extracted from the file.")
        
    print(f"Extracted {len(image_bytes_list)} page(s). Sending to OpenAI for analysis...")
    
    try:
        json_result = extract_info_from_images(image_bytes_list)
        json_result = json_result.strip()

        if json_result.startswith("```"):
            json_result = json_result.removeprefix("```json")
            json_result = json_result.removeprefix("```")
            json_result = json_result.removesuffix("```")
            json_result = json_result.strip()
        
    except openai.RateLimitError as e:
        print(f"\n[ERROR] OpenAI Rate Limit / Quota Exceeded:")
        print(f"Details: {e.message}")
        print("\nPlease check your OpenAI billing plan and ensure you have active credits at https://platform.openai.com/api-keys")
        return
    except Exception as e:
        print(f"\n[ERROR] Failed to extract information via OpenAI: {e}")
        return
    
    # Parse the returned string into a JSON object to pretty-print
    try:
        data = json.loads(json_result)
        
        # Save output to a JSON file
        output_file = os.path.splitext(PATH)[0] + "_extracted.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        print("\nExtraction Successful! Extracted JSON content:\n")
        print(json.dumps(data, indent=4, ensure_ascii=False))
        print(f"\nResults saved to: {output_file}")
    except json.JSONDecodeError:
        print("Failed to decode JSON from OpenAI response:")
        print(json_result)

if __name__ == "__main__":
    main()