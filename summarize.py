from datetime import datetime
import PyPDF2
import json
import re
import requests
import json
import os

def pdf_to_text(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""

        for page in reader.pages:
            text += page.extract_text()

    return text


def call_openai_api(chunk, custom_message, gpt_version, OPENAI_API_KEY):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    data = {
        "model": gpt_version,
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


def generate_summaries(text_chunks, custom_message, max_api_calls, gpt_version, OPENAI_API_KEY):
    summaries = []
    api_calls = 0

    for chunk in text_chunks:
        if api_calls >= max_api_calls:
            break

        summary = call_openai_api(chunk, custom_message, gpt_version, OPENAI_API_KEY)

        if summary:
            token_count = count_tokens(summary)
            summaries.append({
                "original_chunk": chunk,
                "summary": summary,
                "token_count": token_count
            })

            api_calls += 1

    return summaries


def save_summaries_to_json(summaries, directory):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f'summaries_{timestamp}.json'
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, file_name), 'w') as f:
        json.dump(summaries, f)
    return summaries  # return summaries after saving to file


def format_and_save_summaries(summaries, output_directory):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'summaries_formatted_{timestamp}.txt'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    # Extract only the 'summary' field from each entry in the summaries list
    summaries_only = [entry['summary'] for entry in summaries]
    formatted_summaries = [f'Summary {i+1}:<br>{summary}<br><br>' for i, summary in enumerate(summaries_only)]
    formatted_summaries_txt = [f'Summary {i+1}:\n{summary}\n\n' for i, summary in enumerate(summaries_only)]
    with open(os.path.join(output_directory, output_file), 'w', encoding='utf-8') as file:
        for formatted_summary in formatted_summaries_txt:
            file.write(formatted_summary)
    return formatted_summaries