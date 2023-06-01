import PyPDF2
import json
import re
import requests
from secret_key import OPENAI_API_KEY

def pdf_to_text(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""

        for page in reader.pages:
            text += page.extract_text()

    return text


def call_openai_api(chunk, custom_message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": f"{custom_message}{chunk}"}],
        "max_tokens" : 1024,
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        data=json.dumps(data),
    )

    if response.status_code == 200:
        response_data = response.json()
        assistant_message = response_data["choices"][0]["message"]["content"]
        return assistant_message.strip()
    else:
        print("Error:", response.status_code, response.text)
        return None


def count_tokens(text):
    return len(text.split(' '))


def read_custom_message(file_name):
    with open(file_name, "r") as file:
        custom_message = file.read().strip()
    return custom_message


def create_text_chunks(text, max_tokens=1200):
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()

        if count_tokens(current_chunk + ' ' + sentence) > max_tokens:
            chunks.append(current_chunk)
            current_chunk = sentence
        else:
            current_chunk += ' ' + sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def preprocess(text):
    text = re.sub(r'\.{2,}', ' ', text)
    text = text.replace('\n', ' ').strip()
    text = re.sub(r'\s+', ' ', text)

    return text