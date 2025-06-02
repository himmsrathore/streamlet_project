import pandas as pd
import os
from googletrans import Translator

translator = Translator()

filelist = [
    "sample_q.csv",
]

def translate_and_append(text):
    try:
        if pd.isna(text):
            return text
        hindi_translation = translator.translate(text, dest='hi').text
        return f"{text} [ {hindi_translation} ]"
    except Exception as e:
        print(f"Translation error: {e} for text: {text}")
        return text  # If translation fails, return the original text

for file_path in filelist:
    data = pd.read_csv(file_path, encoding='utf-8-sig')

    for index, row in data.iterrows():
        for col in ['question', 'option-1', 'option-2', 'option-3', 'option-4']:
            data.at[index, col] = translate_and_append(row[col])

    modified_file_path = os.path.splitext(file_path)[0] + '_converted.csv'
    data.to_csv(modified_file_path, index=False, encoding='utf-8-sig')

    print("Translation and appending completed. The modified file has been saved for", file_path)
