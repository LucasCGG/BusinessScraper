# BusinessScrapper

BusinessScrapper is a Python-based tool that utilizes the Google Places API to retrieve information about businesses within a specified area.

## Features

- Fetches detailed information about businesses in a given location.
- Supports various search parameters to refine results.
- Outputs data in a structured format for easy analysis.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.6 or higher
- An active Google Cloud account with access to the Places API
- `requests` library (installable via pip)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/LucasCGG/BusinessScrapper.git
   cd BusinessScrapper
   ```

2. **Install the required dependencies:**
   ```bash
    pip install requests
    pip install pandas
   ```

3. **Set up your API key:**
    - Obtain an API key from Google Cloud.
    - Create a .env file in the root directory of the project and add your API key as the value of the `API_KEY` variable.
   ```bash
    GOOGLE_API_KEY=your_api_key_here
   ```

## Usage
1. **Run the script:**
   ```bash
   python scraper.py
   ```

2. **Input Parameters:**
    - `location`: The location to search for businesses (e.g., "New York").
    - `category`: The type of business to search for (e.g., "restaurants").
    - `radius`: The search radius in meters (default is 5000).

3. **Output:**
    The scraper will display the retrieved business information in the console ad save it to a file named `businesses.csv`.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.
Please follow these steps:
1. Fork the repository
2. Create a new branch : `git checkout -b my-new-feature`
3. Make your changes : `git commit -am 'Add some feature'`
4. Push to the branch : `git push origin my-new-feature`
5. Submit a pull request

## License

This project is open-sourced under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Maps API for providing the business data.
- Requests: HTTP For Humans.



