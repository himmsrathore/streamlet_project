import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
import pdfplumber
import os

# Initialize translator
translator = GoogleTranslator(source='en', target='hi')

# Translate and append Hindi
def translate_and_append(text):
    try:
        if pd.isna(text):
            return text
        hindi_translation = translator.translate(text)
        return f"{text} [ {hindi_translation} ]"
    except Exception as e:
        st.error(f"Translation error: {e} for text: {text}")
        return text

# CSV Processing Function
def process_csv(file):
    try:
        data = pd.read_csv(file, encoding='utf-8-sig')
        for col in ['question', 'option-1', 'option-2', 'option-3', 'option-4']:
            if col in data.columns:
                data[col] = data[col].apply(translate_and_append)
        output_file = "converted_output.csv"
        data.to_csv(output_file, index=False, encoding='utf-8-sig')
        return output_file
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None

# PDF Processing Function
def process_pdf(file):
    try:
        extracted_text = []
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text.extend(text.split('\n'))

        # Create a DataFrame (for example, each line becomes a row)
        df = pd.DataFrame({'Line': extracted_text})
        output_file = "pdf_to_csv_output.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        return output_file
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return None

# Streamlit app
def main():
    st.title("CSV & PDF Converter App")

    project = st.sidebar.selectbox("Select Project", ["Project 1: CSV Converter", "Project 2: PDF to CSV"])

    if project == "Project 1: CSV Converter":
        st.header("Project 1: English to Hindi CSV Converter")
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
        if uploaded_file is not None:
            st.write("File uploaded successfully!")
            if st.button("Convert CSV"):
                with st.spinner("Converting..."):
                    output_file = process_csv(uploaded_file)
                if output_file:
                    with open(output_file, "rb") as file:
                        st.download_button(
                            label="Download Converted CSV",
                            data=file,
                            file_name="converted_output.csv",
                            mime="text/csv"
                        )
                    st.success("Conversion completed!")
                    if os.path.exists(output_file):
                        os.remove(output_file)

    elif project == "Project 2: PDF to CSV":
        st.header("Project 2: Convert PDF to CSV")
        uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
        if uploaded_pdf is not None:
            st.write("PDF uploaded successfully!")
            if st.button("Convert PDF to CSV"):
                with st.spinner("Extracting text and converting..."):
                    output_file = process_pdf(uploaded_pdf)
                if output_file:
                    with open(output_file, "rb") as file:
                        st.download_button(
                            label="Download Extracted CSV",
                            data=file,
                            file_name="pdf_to_csv_output.csv",
                            mime="text/csv"
                        )
                    st.success("PDF converted to CSV!")
                    if os.path.exists(output_file):
                        os.remove(output_file)

if __name__ == "__main__":
    main()
