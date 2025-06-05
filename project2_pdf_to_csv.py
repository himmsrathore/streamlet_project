# project2_pdf_to_csv.py

import pdfplumber
import pandas as pd
import streamlit as st
import os
import re

# Remove Hindi (Devanagari) chars from text
def remove_hindi(text):
    return re.sub(r'[\u0900-\u097F]+', '', text).strip()

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
        current_block = []
        
        # Group lines by questions
        for line in all_lines:
            if line.startswith("Question Id :"):
                if current_block:
                    questions.append(current_block)
                current_block = []
            current_block.append(line)
        if current_block:
            questions.append(current_block)

        parsed_data = []
        for block in questions:
            question_lines = []
            options = ["", "", "", ""]
            answer = ""

            i = 0
            # Extract question text lines, skip "Question Id :" line
            while i < len(block) and not block[i].startswith("Answer : Option Id"):
                if not block[i].startswith("Question Id :"):
                    question_lines.append(block[i])
                i += 1

            question_text = " ".join(question_lines).strip()
            question_text = remove_hindi(question_text)  # Remove Hindi chars

            # Skip "Answer : Option Id"
            if i < len(block) and block[i].startswith("Answer : Option Id"):
                i += 1

            # Extract 4 options (remove Hindi from each)
            option_index = 0
            while i < len(block) and option_index < 4:
                line = block[i]
                if re.match(r"\([A-D]\)", line):
                    option_text = re.sub(r"^\([A-D]\)\s*", "", line).strip()
                    option_text = remove_hindi(option_text)
                    options[option_index] = option_text
                    option_index += 1
                i += 1

            # Extract Right Answer (FIXED LOGIC)
            while i < len(block):
                if block[i].startswith("Right Answer :"):
                    # Check if answer is on the same line
                    same_line_answer = block[i].replace("Right Answer :", "").strip()
                    if same_line_answer:
                        answer = remove_hindi(same_line_answer)
                    else:
                        # Answer is on the next line(s)
                        i += 1
                        if i < len(block):
                            answer = remove_hindi(block[i].strip())
                    break
                i += 1

            # Only add if we have complete data
            if question_text and answer and all(opt.strip() for opt in options):
                parsed_data.append({
                    'question': question_text,
                    'option-1': options[0],
                    'option-2': options[1],
                    'option-3': options[2],
                    'option-4': options[3],
                    'answer': answer,
                })

        df = pd.DataFrame(parsed_data)
        df = df[['question', 'option-1', 'option-2', 'option-3', 'option-4', 'answer']]
        
        output_file = "pdf_to_csv_output.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        return output_file, len(parsed_data)

    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return None, 0

def pdf_to_csv_ui():
    st.header("Project 2: Convert PDF to CSV")
    st.markdown("Upload a PDF file containing questions and answers to convert it to CSV format.")
    
    uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if uploaded_pdf is not None:
        st.success("✅ PDF uploaded successfully!")
        
        # Show file details
        file_details = {"Filename": uploaded_pdf.name, "FileType": uploaded_pdf.type, "FileSize": f"{uploaded_pdf.size} bytes"}
        st.write("**File Details:**")
        for key, value in file_details.items():
            st.write(f"- {key}: {value}")
        
        if st.button("Convert PDF to CSV", type="primary"):
            with st.spinner("🔄 Extracting text and converting..."):
                result = process_pdf(uploaded_pdf)
                
            if result[0]:  # If output_file exists
                output_file, question_count = result
                
                with open(output_file, "rb") as file:
                    st.download_button(
                        label="📥 Download Extracted CSV",
                        data=file,
                        file_name="pdf_to_csv_output.csv",
                        mime="text/csv",
                        type="primary"
                    )
                
                st.success(f"🎉 PDF converted to CSV successfully! Extracted {question_count} questions.")
                
                # Show preview of extracted data
                if st.checkbox("Show preview of extracted data"):
                    df = pd.read_csv(output_file)
                    st.dataframe(df.head(), use_container_width=True)
                
                # Clean up
                if os.path.exists(output_file):
                    os.remove(output_file)
            else:
                st.error("❌ Failed to convert PDF. Please check the PDF format and try again.")

    else:
        st.info("👆 Please upload a PDF file to get started.")
        
        # Add some helpful information
        with st.expander("ℹ️ How to use this tool"):
            st.markdown("""
            **Steps to convert your PDF:**
            1. Upload a PDF file containing questions and answers
            2. Click the "Convert PDF to CSV" button
            3. Wait for processing to complete
            4. Download the generated CSV file
            
            **Expected PDF format:**
            - Questions should start with "Question Id :"
            - Multiple choice options should be labeled (A), (B), (C), (D)
            - Correct answers should be marked with "Right Answer :"
            
            **Features:**
            - Automatically removes Hindi/Devanagari text
            - Extracts only English content
            - Handles multi-line questions and answers
            - Generates clean CSV output
            """)

if __name__ == "__main__":
    pdf_to_csv_ui()