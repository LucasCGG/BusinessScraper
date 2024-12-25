import requests
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import time
import re
import tkinter as tk
from tkinter import scrolledtext, messagebox

"""
@Author: Lucas Colaco
@Date: 2024-12-21
@Description: This script fetches business information using the Google Maps API and attempts to extract email addresses from business websites.
@Usage: python scraper.py
@Prerequisites:
    - Python 3.6 or higher
    - An active Google Cloud account with access to the Places API
    - requests and beautifulsoup4 libraries (installable via pip)
@Version: 2.0.0
"""


def fetch_businesses(location, category, api_key, radius=5000):
    """
    Fetch businesses from Google Maps API.

    Args:
        location (str): A string specifying the location (e.g., "New York").
        category (str): Type of business to search for (e.g., "restaurants").
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
                    email = fetch_email_from_website(website) if website else "No website available"
                else:
                    website = "No website available"
                    phone = "No phone available"
                    email = "No email available"

                client_list.append({
                    "Name": name,
                    "Website": website if website else "No website available",
                    "Phone": phone if phone else "No phone available",
                    "Email": email,
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


def fetch_email_from_website(website):
    """
    Scrape email addresses from a given website URL.

    Args:
        website (str): The URL of the website.

    Returns:
        str: A comma-separated string of email addresses or 'No email available'.
    """
    try:
        response = requests.get(website, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Use regex to find email addresses in the page content
        emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", soup.text))
        return ", ".join(emails) if emails else "No email available"
    except Exception as e:
        print(f"Failed to fetch email from {website}: {e}")
        return "No email available"


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


def run_scraper():
    location = location_entry.get()
    category = category_entry.get()
    radius = radius_entry.get()
    radius = int(radius) if radius and radius.isdigit() else 5000

    if not location or not category:
        messagebox.showerror("Input Error", "Please enter both location and category.")
        return

    try:
        businesses = fetch_businesses(location, category, API_KEY, radius)
        if businesses:
            save_to_csv(businesses)  # Save the fetched businesses to a CSV file
            result_text.delete(1.0, tk.END)  # Clear previous results
            for business in businesses:
                result_text.insert(tk.END, f"{'Name:':<30} {business['Name']}\n")
                result_text.insert(tk.END, f"{'Website:':<30} {business['Website']}\n")
                result_text.insert(tk.END, f"{'Phone:':<30} {business['Phone']}\n")
                result_text.insert(tk.END, f"{'Email:':<30} {business['Email']}\n")
                result_text.insert(tk.END, f"{'Address:':<30} {business['Address']}\n")
                result_text.insert(tk.END, "-"*60 + "\n")  # Separator line
            messagebox.showinfo("Success", f"Found {len(businesses)} businesses.")
        else:
            messagebox.showinfo("No Results", "No businesses found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def on_entry_click(event, entry, placeholder):
    """Function to handle entry click event."""
    if entry.get() == placeholder:
        entry.delete(0, tk.END)  # Clear the placeholder
        entry.config(fg='black')  # Change text color to black


def on_focusout(event, entry, placeholder):
    """Function to handle focus out event."""
    if entry.get() == '':
        entry.insert(0, placeholder)  # Restore the placeholder
        entry.config(fg='grey')  # Change text color to grey


def create_gui():
    global location_entry, category_entry, radius_entry, result_text

    window = tk.Tk()
    window.title("Business Scraper")

    # Create a frame for input fields
    input_frame = tk.Frame(window)
    input_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    # Location
    tk.Label(input_frame, text="Location:").pack(anchor='w', padx=16)
    location_entry = tk.Entry(input_frame, fg='grey')
    location_entry.insert(0, "Enter location")
    location_entry.pack(padx=16, fill=tk.X, expand=True)
    location_entry.bind("<FocusIn>", lambda event: on_entry_click(event, location_entry, "Enter location"))
    location_entry.bind("<FocusOut>", lambda event: on_focusout(event, location_entry, "Enter location"))

    # Category
    tk.Label(input_frame, text="Category:").pack(anchor='w', padx=16)
    category_entry = tk.Entry(input_frame, fg='grey')
    category_entry.insert(0, "Enter category")
    category_entry.pack(padx=16, fill=tk.X, expand=True)
    category_entry.bind("<FocusIn>", lambda event: on_entry_click(event, category_entry, "Enter category"))
    category_entry.bind("<FocusOut>", lambda event: on_focusout(event, category_entry, "Enter category"))

    # Radius
    tk.Label(input_frame, text="Radius (meters):").pack(anchor='w', padx=16)
    tk.Label(input_frame, text="Hint: Distance in meters").pack(anchor='w', padx=16)

    radius_entry = tk.Entry(input_frame)
    radius_entry.insert(0, "5000")  # Default value
    radius_entry.pack(padx=16, fill=tk.X, expand=True)

    tk.Button(window, text="Fetch Businesses", command=run_scraper).pack(pady=16)

    result_text = scrolledtext.ScrolledText(window, width=50, height=20)
    result_text.pack(pady=16, padx=16, fill=tk.BOTH, expand=True)

    window.mainloop()


if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.getenv("GOOGLE_API_KEY")
    create_gui()
