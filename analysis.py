import streamlit as st
import requests
import csv
import os
from datetime import datetime

def perform_rag(query, api_key):
    headers = {"X-API-Key": api_key}
    response = requests.get(
        f"https://api.ydc-index.io/rag?query={query}",
        headers=headers
    )
    return response.json()

def append_to_csv(file_path, username, query, answer):
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if file exists, if not, create it with headers
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        if not file_exists:
            writer.writerow(['Timestamp', 'Username', 'Query', 'Answer'])  # Writing headers
        writer.writerow([timestamp, username, query, answer])

st.title('Question Interface')

username = st.text_input('Enter your username')
query = st.text_area('Enter your question')
api_key = st.secrets["auth_token"]  # Replace with your actual API key
csv_file_path = 'storage.csv'  # Replace with your preferred file name

# Check if both username and query are provided
if username and query:
    if st.button('Submit'):
        response = perform_rag(query, api_key)
        answer = response.get('answer', 'No answer found')  # Extract the answer
        st.text('Result:')
        st.write(answer)

        # Append username, query, and answer to CSV with timestamp
        append_to_csv(csv_file_path, username, query, answer)

# Show download button only if the CSV file exists
if os.path.isfile(csv_file_path):
    with open(csv_file_path, "rb") as file:
        st.download_button(
            label="Download CSV File",
            data=file,
            file_name=csv_file_path,
            mime="text/csv"
        )
