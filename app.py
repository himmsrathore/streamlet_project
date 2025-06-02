import streamlit as st
import pandas as pd
from googletrans import Translator
import os

# Initialize the translator
translator = Translator()

# Function to translate text to Hindi and append
def translate_and_append(text):
    try:
        if pd.isna(text):
            return text
        hindi_translation = translator.translate(text, dest='hi').text
        return f"{text} [ {hindi_translation} ]"
    except Exception as e:
        st.error(f"Translation error: {e} for text: {text}")
        return text  # Return original text if translation fails

# Function to process the uploaded CSV
def process_csv(file):
    try:
        # Read the uploaded CSV
        data = pd.read_csv(file, encoding='utf-8-sig')
        
        # Translate specified columns
        for col in ['question', 'option-1', 'option-2', 'option-3', 'option-4']:
            if col in data.columns:
                data[col] = data[col].apply(translate_and_append)
        
        # Save the converted data to a temporary file
        output_file = "converted_output.csv"
        data.to_csv(output_file, index=False, encoding='utf-8-sig')
        return output_file
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None

# Streamlit app
def main():
    # Set page title
    st.title("CSV Converter App")

    # Sidebar for project selection
    project = st.sidebar.selectbox("Select Project", ["Project 1: CSV Converter", "Project 2: In Development"])

    if project == "Project 1: CSV Converter":
        st.header("Project 1: English to Hindi CSV Converter")
        
        # File uploader
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
        
        if uploaded_file is not None:
            st.write("File uploaded successfully!")
            
            # Process the file when the user clicks the button
            if st.button("Convert CSV"):
                with st.spinner("Converting..."):
                    output_file = process_csv(uploaded_file)
                
                if output_file:
                    # Provide download button for the converted file
                    with open(output_file, "rb") as file:
                        st.download_button(
                            label="Download Converted CSV",
                            data=file,
                            file_name="converted_output.csv",
                            mime="text/csv"
                        )
                    st.success("Conversion completed! Download the file using the button above.")
                    
                    # Clean up temporary file
                    if os.path.exists(output_file):
                        os.remove(output_file)
        
    elif project == "Project 2: In Development":
        st.header("Project 2: In Development")
        st.write("This project is currently under development. Stay tuned for updates!")

if __name__ == "__main__":
    main()