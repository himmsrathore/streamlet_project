import pdfplumber
import pandas as pd
import re

# Remove Hindi (Devanagari) chars from text
def remove_hindi(text):
    return re.sub(r'[\u0900-\u097F]+', '', text).strip()

def parse_pdf_only_english(file_path):
    try:
        all_lines = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    lines = text.strip().split('\n')
                    all_lines.extend(lines)

        questions = []
        current_block = []
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

        output_file = "output_only_english.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"✅ Saved {len(parsed_data)} questions to {output_file}")
        
        # Print first few rows to verify
        print("\n📋 First few rows:")
        print(df.head().to_string(index=False))

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python parse_pdf_only_english.py path/to/file.pdf")
    else:
        pdf_path = sys.argv[1]
        parse_pdf_only_english(pdf_path)