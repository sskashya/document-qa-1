import streamlit as st
from openai import OpenAI
import openai
import pymupdf
import fitz

# Show title and description.
st.title("MY Document question answering - HW1")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)
    try:
        client.models.list()
    except openai.AuthenticationError:
        st.info("Invalid API Key. Try again")
    else:
    # Let the user upload a file via `st.file_uploader`.
        uploaded_file = st.file_uploader("Upload a document (.txt or .pdf)", type=("txt", "pdf"))

        if uploaded_file:
            file_extension = uploaded_file.name.split('.')[-1]
            if file_extension == 'txt':
                document = uploaded_file.read().decode()
            elif file_extension == 'pdf':
                text = ''
                with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                    for page_num in range(len(doc)):
                        page = doc.load_page(page_num)
                        text += page.get_text()
                document = text
            else:
                st.error("Unsupported file type.")

        # Ask the user for a question via `st.text_area`.
            question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
        )
            if uploaded_file and question:
        # Process the uploaded file and question.
                messages = [
        {
            "role": "user",
            "content": f"Here's a document: {document} \n\n---\n\n {question}",
        }
    ]
        # Generate an answer using the OpenAI API.
                stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
        )
        # Stream the response to the app using `st.write_stream`.
                st.write_stream(stream)

