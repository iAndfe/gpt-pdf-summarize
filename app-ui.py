import gradio as gr
from datetime import datetime
import summarize
import warnings

# Ignore deprecation warnings
warnings.filterwarnings('ignore', category=UserWarning)

custom_message = summarize.read_custom_message('custom_message.txt')


def summarize_pdf(custom_message, gpt_version, max_api_calls, openai_api_key, pdf_file):
    # check if the API key is provided
    if not openai_api_key or openai_api_key == 'your-openai-api-key':
        return 'Please provide a valid OpenAI API Key.'

    # make sure the uploaded file is a PDF
    if not pdf_file.name.endswith(".pdf"):
        return 'Please upload a PDF file.'

    # read the PDF contents
    file_path = pdf_file.name

    # pdf_to_text, preprocess and create_text_chunks can be defined in your summarize.py file
    text = summarize.pdf_to_text(file_path)
    preprocessed_text = summarize.preprocess(text)
    text_chunks = summarize.create_text_chunks(preprocessed_text)

    # generate summaries
    summaries = summarize.generate_summaries(
        text_chunks,
        custom_message,
        max_api_calls,
        gpt_version,
        openai_api_key
    )

    # Save summaries to JSON file and also get it in the python variable
    summaries = summarize.save_summaries_to_json(summaries, 'processed')

    # Now call your function with the summaries and the output directory
    formatted_summaries = summarize.format_and_save_summaries(summaries, 'processed')

    return formatted_summaries


# Define the Gradio interface
iface = gr.Interface(
    fn=summarize_pdf,  # the function to wrap
    inputs=[
        gr.inputs.Textbox(lines=10, default = custom_message, label="Custom Message"),
        gr.inputs.Dropdown(["gpt-3.5-turbo", "gpt-4"], default = "gpt-4", label="GPT Version"),
        gr.inputs.Number(default=50, label="Max API Calls"),
        gr.inputs.Textbox(default="your-openai-api-key", label="OpenAI API Key"),
        gr.inputs.File(label="PDF File"),
    ],
    outputs=gr.outputs.HTML(label="Summaries"),
)

# Start the interface
iface.launch()