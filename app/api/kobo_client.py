import os
import requests
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
    """
    Fetches data from KoboToolbox API and handles large datasets using pagination.

    Args:
        page_size (int): The number of records to fetch per page (default is set by PAGE_SIZE).

    Returns:
        list: A list of records fetched from the KoboToolbox API.
    """
    records = []
    next_url = KOBO_API_URL  # Start with the initial URL
    params = {
        'page_size': page_size
    }

    while next_url:
        try:
            response = requests.get(next_url, headers=HEADERS, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors

            data = response.json()
            records.extend(data['results'])  # Append new data to the records list

            # Check if there is a next page
            next_url = data.get('next')
            if next_url:
                print(f"Fetching next page: {next_url}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break

    return records

if __name__ == "__main__":
    data = fetch_data_from_kobo()
    print(f"Total records fetched: {len(data)}")
    # Print the first few records for inspection
    print(data[:5])
