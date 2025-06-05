import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
import os

translator = GoogleTranslator(source='en', target='hi')

def translate_and_append(text):
    try:
        if pd.isna(text):
            return text
        hindi_translation = translator.translate(text)
        return f"{text} [ {hindi_translation} ]"
    except Exception as e:
        st.error(f"Translation error: {e} for text: {text}")
        return text

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

def csv_converter_ui():
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
