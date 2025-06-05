import streamlit as st
import pandas as pd
import pdfplumber
import os

def process_pdf(file):
    try:
        extracted_text = []
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text.extend(text.split('\n'))

        df = pd.DataFrame({'Line': extracted_text})
        output_file = "pdf_to_csv_output.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        return output_file
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return None

def pdf_to_csv_ui():
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
