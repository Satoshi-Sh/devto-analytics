import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://dev.to/api"
API_KEY = os.getenv("DEVTO_API_KEY")

# Check if API key is loaded
if not API_KEY:
    raise ValueError("API key not found. Ensure the .env file is correctly configured.")

headers = {
    "api-key": API_KEY,
}


def get_data():
    response = requests.get(f"{BASE_URL}/articles/me?per_page=1000", headers=headers)
    # Check for response status
    if response.status_code == 401:
        print("Unauthorized: Check your API key.")
        return
    elif response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return
    data = response.json()
    return data
