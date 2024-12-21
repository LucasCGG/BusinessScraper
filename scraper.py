import requests
import pandas as pd
from dotenv import load_dotenv
import os
import time

"""
@Author: Lucas Colaco
@Date: 2024-12-21
@Description: This script is a Python implementation of a business scraper that uses the Google Maps API to fetch information about businesses in a specified location.
@Usage: python scraper.py
@Prerequisites: 
    - Python 3.6 or higher
    - An active Google Cloud account with access to the Places API
    - requests library (installable via pip)
@Version: 1.0.0
"""


def fetch_businesses(location, category, api_key, radius=5000):
    """
    Fetch businesses from Google Maps API.

    Args:
        location (str): A string specifying the location (e.g., "New York").
        category (str): Type of business to search for (eAPI.g., "restaurants").
        api_key (str): Your Google Maps API key.
        radius (int): Search radius in meters (default is 5000).

    Returns:
        list: A list of businesses with their details.
    """
    textsearch_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    params = {
        "query": f"{category} in {location}",
        "key": api_key,
        "radius": radius
    }

    client_list = []

    while True:
        response = requests.get(textsearch_url, params=params)

        if response.status_code == 200:
            data = response.json()
            businesses = data.get("results", [])

            for business in businesses:
                name = business.get("name")
                address = business.get("formatted_address")
                place_id = business.get("place_id")

                # Fetch additional details like website and phone using Place Details API
                details_params = {
                    "place_id": place_id,
                    "fields": "name,website,formatted_phone_number",
                    "key": api_key
                }

                details_response = requests.get(details_url, params=details_params)

                if details_response.status_code == 200:
                    details_data = details_response.json().get("result", {})
                    website = details_data.get("website")
                    phone = details_data.get("formatted_phone_number")
                else:
                    website = "No website available"
                    phone = "No phone available"

                client_list.append({
                    "Name": name,
                    "Website": website if website else "No website available",
                    "Phone": phone if phone else "No phone available",
                    "Address": address,
                })

            # Handle pagination if there is a next page
            next_page_token = data.get("next_page_token")
            if next_page_token:
                params["pagetoken"] = next_page_token
                # Delay is required for the next page token to become valid
                time.sleep(2)
            else:
                break
        else:
            print(f"Error fetching data: {response.status_code}")
            break

    return client_list

def save_to_csv(data, filename="businesses.csv"):
    """
    Save data to a CSV file.

    Args:
        data (list): List of dictionaries with business data.
        filename (str): Name of the output CSV file.
    """
    if data:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, sep=';')
    else:
        print("No data to save.")

def main():
    load_dotenv()

    API_KEY = os.getenv("GOOGLE_API_KEY")
    location = input("Enter the location (e.g., 'New York'): ")
    category = input("Enter the category of businesses (e.g., 'restaurants'): ")
    radius = input("Enter the search radius in meters or press enter to default to 5000: ")
    radius = int(radius) if radius else 5000

    print("Fetching businesses...")
    businesses = fetch_businesses(location, category, API_KEY, radius)

    if businesses:
        print(f"Found {len(businesses)} businesses.")
        save_to_csv(businesses)
    else:
        print("No businesses found.")

if __name__ == "__main__":
    main()
