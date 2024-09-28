![websc](https://github.com/user-attachments/assets/647b4afc-eabf-4f70-9950-56c3c99b568d)


# BravoCyberScraper

## Overview

BravoCyberScraper is a Python-based web scraper designed to extract job listings specifically for entry-level cybersecurity positions in the USA. It uses the jSearch API to gather job data, which includes essential details such as job title, employer, location, and more. The results are stored in JSON format and can also be exported to a CSV file for easy analysis.


##Features

Fetches entry-level cybersecurity jobs from the jSearch API.
Supports various query parameters such as job type, location, and salary.
Logs detailed information about the scraping process for easier debugging and tracking.
Outputs job listings in both JSON and CSV formats.

## Requirements
Before running the scraper, ensure you have the following installed:


Python 3.x
Libraries:
requests
pandas
json
time
logging

###You can install the required libraries using pip:

bash

Copy code

pip install requests pandas

##Configuration

API Key: The script requires a valid API key to access the jSearch API. 
Replace the placeholder API key in the code with your actual key:

### python

Copy code

HEADERS = {
    "x-rapidapi-key": "YOUR_API_KEY_HERE",
    "x-rapidapi-host": "jsearch.p.rapidapi.com"
}
Query Parameters: You can adjust the QUERY_PARAMS dictionary to customize your search criteria:

query: Search term (default: "entry-level cybersecurity").
date_posted: Filter jobs based on posting date.
remote_jobs_only: Set to "true" to filter remote jobs.
employment_types: Specify the types of employment you're interested in (e.g., "FULLTIME,PARTTIME").
experience_level: Filter jobs based on experience level (default: "entry_level,internship").
location: Set your desired job location (default: "USA").
salary: Set a salary filter (default: 100000).
Usage
To run the scraper, execute the script:

bash
Copy code
python bravoscraper.py
Steps Performed by the Script
Extract Listings: The script fetches job listings based on the defined query parameters and stores them in a JSON file (job_listings.json).
Convert JSON to DataFrame: The JSON file is then converted into a pandas DataFrame for easier manipulation and analysis.
Clean DataFrame: The DataFrame is cleaned by renaming columns, handling missing values, and standardizing certain fields.
Save to CSV: Finally, the cleaned DataFrame is saved as a CSV file (job_listings.csv).
Logging
The script includes logging functionality to track the scraping process. Logs will be written to a file named job_scraper.log and can also be viewed in the console.

Notes
The script is designed to fetch a limited number of job postings per API call. You can adjust the num_pages parameter to scrape more pages if needed.
Ensure to adhere to the API's rate limits to avoid being blocked.
License
This project is licensed under the MIT License. See the LICENSE file for more details.

Contributions
Contributions are welcome! Please feel free to fork the repository and submit a pull request for any improvements or features you'd like to add.

