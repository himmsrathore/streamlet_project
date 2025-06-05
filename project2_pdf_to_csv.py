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

                # Extract question lines until "Answer : Option Id"
                while i < len(all_lines) and not all_lines[i].startswith("Answer : Option Id"):
                    question_text += all_lines[i] + " "
                    i += 1
                question_text = question_text.strip()

                # Move past "Answer : Option Id"
                i += 1

                # Extract 4 options
                options = []
                while i < len(all_lines) and re.match(r"\([A-D]\)", all_lines[i]):
                    line = all_lines[i]
                    option_text = re.sub(r"\([A-D]\)\s*", "", line)  # Remove (A), (B), etc.
                    option_text = re.sub(r"\d+$", "", option_text).strip()  # Remove trailing IDs
                    options.append(option_text)
                    i += 1

                # Extract Right Answer
                answer = ""
                while i < len(all_lines) and not all_lines[i].startswith("Right Answer :"):
                    i += 1
                if i < len(all_lines) and all_lines[i].startswith("Right Answer :"):
                    answer = all_lines[i].replace("Right Answer :", "").strip()
                    i += 1  # Skip to next block

                # Only add complete entries
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
