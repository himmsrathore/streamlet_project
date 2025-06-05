# project2_pdf_to_csv.py

import pdfplumber
import pandas as pd
import streamlit as st
import os
import re

def process_pdf(file):
    try:
        all_lines = []
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    lines = text.strip().split('\n')
                    all_lines.extend(lines)

        questions = []
        i = 0
        while i < len(all_lines):
            if all_lines[i].startswith("Question Id :"):
                i += 1
                question_text = ""

                # Collect lines for the question
                while i < len(all_lines) and not all_lines[i].startswith("Answer : Option Id"):
                    question_text += all_lines[i] + " "
                    i += 1
                question_text = question_text.strip()

                # Skip "Answer : Option Id"
                i += 1

                # Extract 4 options
                options = []
                while i < len(all_lines) and re.match(r"\([A-D]\)", all_lines[i]):
                    line = all_lines[i]
                    option_text = re.sub(r"\([A-D]\)\s*", "", line)
                    option_text = re.sub(r"\d+$", "", option_text).strip()
                    options.append(option_text)
                    i += 1

                # Find the correct answer
                answer = ""
                while i < len(all_lines) and not all_lines[i].startswith("Right Answer :"):
                    i += 1
                if i < len(all_lines) and all_lines[i].startswith("Right Answer :"):
                    answer = all_lines[i].replace("Right Answer :", "").strip()
                    i += 1

                if len(options) == 4 and question_text and answer:
                    questions.append({
                        'question': question_text,
                        'answer': answer,
                        'option-1': options[0],
                        'option-2': options[1],
                        'option-3': options[2],
                        'option-4': options[3],
                    })

            else:
                i += 1

        df = pd.DataFrame(questions)
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
