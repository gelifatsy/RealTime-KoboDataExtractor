import os
import requests
import pandas as pd  # Import pandas for data manipulation
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch configuration from environment variables
KOBO_API_URL = os.getenv("KOBO_API_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
DJANGO_LANGUAGE = os.getenv("DJANGO_LANGUAGE", "en")
PAGE_SIZE = int(os.getenv("PAGE_SIZE", 100))

HEADERS = {
    'Authorization': f'Token {AUTH_TOKEN}',
    'Cookie': f'django_language={DJANGO_LANGUAGE}'
}

def fetch_data_from_kobo(page_size=PAGE_SIZE):
    records = []
    next_url = KOBO_API_URL
    params = {
        'page_size': page_size
    }

    while next_url:
        try:
            response = requests.get(next_url, headers=HEADERS, params=params)
            response.raise_for_status()

            data = response.json()
            records.extend(data['results'])

            next_url = data.get('next')
            if next_url:
                print(f"Fetching next page: {next_url}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break

    return records

def save_data_to_csv(data, file_path='extracted_data.csv'):
    if not data:
        print("No data to save.")
        return

    # Create a DataFrame from the records
    df = pd.DataFrame(data)

    # Convert lists to strings if any
    for column in df.columns:
        if df[column].dtype == 'object':
            df[column] = df[column].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

    # Save the DataFrame to a CSV file
    df.to_csv(file_path, index=False, encoding='utf-8')
    print(f"Data saved to {file_path}")

if __name__ == "__main__":
    data = fetch_data_from_kobo()
    print(f"Total records fetched: {len(data)}")
    print(data[:5])

    # Specify the full path including the filename
    save_path = './data/extracted_data.csv'  # Ensure the directory exists
    save_data_to_csv(data, save_path)
