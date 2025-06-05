from deep_translator import GoogleTranslator
import pdfplumber
import pandas as pd
import streamlit as st
import os
import re

translator = GoogleTranslator(source='en', target='hi')

def translate(text):
    try:
        return f"{text} [ {translator.translate(text)} ]"
    except Exception:
        return text

def process_pdf(file):
    try:
        # Read and flatten lines
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
                question_text = ""
                i += 1
                # Gather question (until "Answer : Option Id")
                while i < len(all_lines) and not all_lines[i].startswith("Answer : Option Id"):
                    question_text += all_lines[i] + " "
                    i += 1
                question_text = question_text.strip()

                # Gather options
                options = []
                if i < len(all_lines) and all_lines[i].startswith("Answer : Option Id"):
                    i += 1
                    while i < len(all_lines) and re.match(r"\([A-D]\)", all_lines[i]):
                        option_line = all_lines[i]
                        option_text = re.sub(r"\([A-D]\)\s*", "", option_line)
                        # Remove trailing digits like "1001001"
                        option_text = re.sub(r"\d+$", "", option_text).strip()
                        options.append(option_text)
                        i += 1

                # Find the right answer
                answer_text = ""
                while i < len(all_lines) and not all_lines[i].startswith("Right Answer :"):
                    i += 1
                if i < len(all_lines) and all_lines[i].startswith("Right Answer :"):
                    answer_text = all_lines[i].replace("Right Answer :", "").strip()
                    i += 1  # Skip the answer explanation line too if needed

                if len(options) == 4:
                    questions.append({
                        'question': translate(question_text),
                        'answer': translate(answer_text),
                        'option-1': translate(options[0]),
                        'option-2': translate(options[1]),
                        'option-3': translate(options[2]),
                        'option-4': translate(options[3])
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
