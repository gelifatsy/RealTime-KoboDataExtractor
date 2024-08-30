import requests

# Define constants for the API endpoint and authorization
KOBO_API_URL = "https://kf.kobotoolbox.org/api/v2/assets/aW9w8jHjn4Cj8SSQ5VcojK/data.json"
AUTH_TOKEN = "f24b97a52f76779e97b0c10f80406af5e9590eaf"
HEADERS = {
    'Authorization': f'Token {AUTH_TOKEN}',
    'Cookie': 'django_language=en'
}

def fetch_data_from_kobo(page_size=100):
    """
    Fetches data from KoboToolbox API and handles large datasets using pagination.

    Args:
        page_size (int): The number of records to fetch per page (default is 100).

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
            next_url = data['next']
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
