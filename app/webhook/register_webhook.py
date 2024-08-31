# app/webhook/register_webhook.py

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the registration URL and webhook URL from environment variables
registration_url = os.getenv("WEBHOOK_REGISTRATION_URL")
webhook_url = os.getenv("WEBHOOK_URL")

# Payload for the registration request
payload = json.dumps({
    "url": webhook_url
})

# Headers for the request
headers = {
    'Content-Type': 'application/json'
}

# Make the POST request to register the webhook
try:
    response = requests.post(registration_url, headers=headers, data=payload)
    
    # Check the response status code and print the result
    if response.status_code == 200:
        print("Webhook registered successfully.")
        print("Response:", response.text)
    else:
        print("Failed to register webhook. Status Code:", response.status_code)
        print("Response:", response.text)
except requests.exceptions.RequestException as e:
    print(f"An error occurred while registering the webhook: {e}")
