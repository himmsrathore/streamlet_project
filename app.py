import streamlit as st
from project1_csv_converter import csv_converter_ui
from project2_pdf_to_csv import pdf_to_csv_ui

def main():
    st.title("CSV & PDF Converter App")

    project = st.sidebar.selectbox("Select Project", [
        "Project 1: CSV Converter",
        "Project 2: PDF to CSV"
    ])

    if project == "Project 1: CSV Converter":
        csv_converter_ui()
    elif project == "Project 2: PDF to CSV":
        pdf_to_csv_ui()

if __name__ == "__main__":
    main()
