# Simplified PDF Summarization Using GPT-4 (by GPT-4 and Andy Feng)

The goal of the script above is to extract information from a PDF document and provide a summarized version of the content using OpenAI's GPT-4 model. This script does so by converting the PDF to plain text, dividing the text into manageable chunks, feeding these chunks to the GPT-4 model via OpenAI API, and gathering the summarized results. Here is an intuitive step-by-step explanation of the process.

1. **PDF to Text**: The `pdf_to_text` function opens a given PDF file and reads its contents. It uses the `PyPDF2` library to extract text from each page and compiles it into one large string.

2. **Preprocessing**: The `preprocess` function is used to clean up the extracted text. It removes extra spaces, replaces line breaks with spaces, and deals with sequences of periods which often represent pauses in the context of the text.

3. **Text Chunking**: The `create_text_chunks` function splits the preprocessed text into smaller chunks. Each chunk has approximately 1200 tokens (roughly equal to words) to make them manageable for the GPT-4 model.

4. **Loading Custom Message**: A custom message for the AI model is read from a separate file by `read_custom_message` function. This message can be used to guide the model in producing the summary.

5. **GPT-4 API Calls**: Each chunk is sent to the GPT-4 model via OpenAI's API by the `call_openai_api` function. The API returns a message generated by the model. The function sends a POST request to the OpenAI API endpoint and includes the chunk, along with the custom message, as data. The response contains the model-generated content, which is extracted and returned.

6. **Summary Extraction and Token Counting**: For each chunk, a summary is generated and its token count is noted. This information is stored in a list of dictionaries. To ensure we don't exceed the maximum allowed API calls, a counter is maintained.

7. **Saving the Summaries**: The summaries are then saved into a JSON file. An output directory is created if it doesn't already exist. Each summary, along with the original chunk and token count, is saved in this file.

8. **Formatting and Saving Summaries in a Text File**: The saved JSON file is opened, and the summaries are extracted and saved in a neatly formatted text file. The output here is designed to be human-readable.

In summary, this script automatically extracts, preprocesses, and summarizes text from PDF files using GPT-4, making it an invaluable tool for quickly understanding the main points of a large document.

# Installation & Usage Guide

## Prerequisites

- **Python**: Make sure Python is installed on your system. If you haven't installed Python, you can download it from the [official Python website](https://www.python.org/downloads/). As of my training cut-off in September 2021, Python 3.9.x is the latest version. Make sure to select the option "Add Python to PATH" during the installation.

- **Visual Studio Code (VS Code)**: This is a free and open-source editor that supports Python and many other programming languages. You can download it from the [official VS Code website](https://code.visualstudio.com/download). 

## Steps to Run the Script

1. **Install Required Python Libraries**: Open your terminal or command prompt, navigate to the directory containing the script, and install the required Python libraries using the pip package manager:

    ```
    pip install PyPDF2 requests
    ```

2. **Setting up OpenAI API Key**: 

    - First, you need to get your OpenAI API Key. To do this, go to the [OpenAI platform](https://beta.openai.com/signup/), sign up and navigate to the API section. Copy your key.
    
    - Create a file named `secret_key.py` in the same directory as your script and write the following line in it (replace "your-api-key" with the key you copied):

        ```python
        OPENAI_API_KEY = "your-api-key"
        ```

3. **Prepare your PDF File and Custom Message File**: 

    - Place your PDF file in the same directory as your script or adjust the file path in the script to match the location of your PDF file.

    - Create a `custom_message.txt` file in the same directory as your script. Write the custom message that you want to send to the GPT-4 model in this file.

4. **Run the Script**: You can now run the steps in the notebook (main.ipynb). To do this, make sure you have python extensions installed on VSCode.

5. **Check the Results**: If everything goes as expected, the script will create a new directory named "processed". Inside this directory, you will find a file named "summaries.json" and "summaries_formatted" containing the summaries of the chunks from your PDF file. There will also be a "summaries_formatted.txt" file, which is a neatly formatted text file containing the same summaries.

Please note that this is a basic guide and assumes you're familiar with running Python scripts and working in a code editor like VS Code. You should also refer to the official OpenAI API and the Python package documentation for the most up-to-date information.
