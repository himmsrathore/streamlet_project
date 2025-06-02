import pandas as pd
import os
from englisttohindi.englisttohindi import EngtoHindi

# Load the CSV file with UTF-8 encoding
# file_path = 'output.csv'  # Replace with your input file path

filelist = [
"grsr.csv",
]

for file_path in filelist:

    data = pd.read_csv(file_path, encoding='utf-8-sig')

    # Define a function to translate and append Hindi text for the entire sentence
    def translate_and_append(text):
        try:
            hindi_translation = EngtoHindi(text).convert
            return f"{text} [ {hindi_translation} ]"
        except Exception as e:
            return text  # If translation fails, return the original text

    # Iterate over each row and translate the question and options
    for index, row in data.iterrows():
        data.at[index, 'question'] = translate_and_append(row['question'])
        data.at[index, 'option-1'] = translate_and_append(row['option-1'])
        data.at[index, 'option-2'] = translate_and_append(row['option-2'])
        data.at[index, 'option-3'] = translate_and_append(row['option-3'])
        data.at[index, 'option-4'] = translate_and_append(row['option-4'])

    # Save the modified DataFrame to a new CSV file with UTF-8 encoding
    modified_file_path = os.path.splitext(file_path)[0] + '_converted.csv'
    data.to_csv(modified_file_path, index=False, encoding='utf-8-sig')

    print("Translation and appending completed. The modified file has been saved for" , file_path)
