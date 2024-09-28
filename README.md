# Zen
Entry-Level Cybersecurity Job Scraper

Table of Contents
Overview
Features
Prerequisites
Installation
Configuration
Usage
Output
Troubleshooting
Contributing
License
Acknowledgments
Overview
The Entry-Level Cybersecurity Job Scraper is a Python-based tool designed to automate the process of fetching, cleaning, and storing job listings specifically tailored for entry-level positions in the cybersecurity field within the USA. Leveraging the jSearch API via RapidAPI, this scraper efficiently gathers relevant job postings, processes the data, and exports it into a structured CSV format for easy analysis and application.

Features
Automated Job Fetching: Retrieves job listings for entry-level cybersecurity positions.
Data Cleaning: Processes and cleans the fetched data to ensure consistency and usability.
CSV Export: Saves the cleaned data into a CSV file for further analysis or record-keeping.
Comprehensive Logging: Tracks the scraping process and logs errors for easy debugging.
Configurable Parameters: Allows customization of search parameters such as location, employment type, and experience level.
Prerequisites
Before setting up the scraper, ensure you have the following:

Python 3.6 or higher installed on your system. You can download it from the official website.
A RapidAPI account with access to the jSearch API.
Basic knowledge of Python and command-line operations.
Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/entry-level-cybersecurity-job-scraper.git
cd entry-level-cybersecurity-job-scraper
Create a Virtual Environment (Optional but Recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Required Libraries:

bash
Copy code
pip install -r requirements.txt
Note: If requirements.txt is not provided, you can install the necessary libraries individually:

bash
Copy code
pip install requests pandas
Configuration
1. API Key Setup
To securely handle your RapidAPI key, it's recommended to use environment variables. However, as per your request, the API key is hardcoded in the script. Ensure that this script is kept private and never shared publicly.

⚠️ Security Warning:
Hardcoding API keys directly into scripts is not recommended due to security risks.
Use environment variables or secret management tools to handle sensitive information.

2. Script Configuration
Open the job_scraper.py script and locate the HEADERS dictionary:

python
Copy code
# Define headers with your API key
HEADERS = {
    "x-rapidapi-key": "API",
    "x-rapidapi-host": "jsearch.p.rapidapi.com"
}
Replace the API key value with your actual RapidAPI key if it's different.

3. Adjusting Query Parameters
The QUERY_PARAMS dictionary defines the search criteria. Modify these parameters as needed:

python
Copy code
# Query parameters tailored for entry-level cybersecurity jobs in the USA
QUERY_PARAMS = {
    "query": "entry-level cybersecurity",
    "date_posted": "all",  # Options might include 'all', '24h', '3d', etc.
    "remote_jobs_only": "false",  # 'true' or 'false' as strings
    "employment_types": "FULLTIME,PARTTIME,INTERN,CONTRACTOR",  # Comma-separated without spaces
    "experience_level": "entry_level,internship",  # Adjusted parameter name
    "location": "USA",
    "page": "1",
    "limit": "20"  # Number of jobs per page (adjust based on API limits)
}
Tips:

query: Define the job title or keywords.
date_posted: Filter jobs based on how recently they were posted.
remote_jobs_only: Set to "true" to fetch only remote jobs.
employment_types: Specify the type of employment.
experience_level: Filter based on required experience.
location: Specify the job location.
page & limit: Control pagination and the number of results per request.
Usage
Ensure Dependencies are Installed:

Make sure you've installed all required libraries as per the Installation section.

Run the Script:

bash
Copy code
python job_scraper.py
The script will perform the following actions:

Fetch job listings based on the defined query parameters.
Convert the fetched JSON data into a Pandas DataFrame.
Clean and process the DataFrame to ensure consistency.
Export the cleaned data into a job_listings.csv file.
Monitor Logs:

The script logs its progress and any errors to both the console and the job_scraper.log file. Review these logs to ensure the scraper is functioning correctly.

Output
Upon successful execution, the following files will be generated:

job_listings.json:
Contains the raw job listings data fetched from the API.

job_listings.csv:
A cleaned CSV file with structured data, ready for analysis or record-keeping.

Sample Columns:

Job Title
Company
Location
Remote
Employment Type
Date Posted
URL
Description
Key Skills
Country
Experience Level
Troubleshooting
1. HTTP 400 Bad Request Error
Error Message:

vbnet
Copy code
ERROR:root:HTTP error occurred on page 1: 400 Client Error: Bad Request for url: ...
WARNING:root:No jobs were fetched.
ERROR:root:Failed to extract job listings. Exiting.
Possible Causes:

Incorrect API endpoint.
Malformed or unsupported query parameters.
Invalid parameter values.
Solutions:

Verify API Endpoint:
Ensure you're using the correct endpoint (/search instead of /search-filters).

Check Query Parameters:
Review and adjust the QUERY_PARAMS to align with the jSearch API Documentation. Ensure parameter names and values are correct.

Test with Minimal Parameters:
Reduce the number of parameters to the essentials and gradually add more to identify the problematic one.

Example Minimal Query:

python
Copy code
QUERY_PARAMS = {
    "query": "entry-level cybersecurity",
    "page": "1",
    "limit": "5"
}
2. DataFrame Cleaning Errors
Error Message:

less
Copy code
ERROR:root:Error cleaning DataFrame: "['Company', 'Remote', 'Employment Type', 'Date Posted', 'Key Skills', 'Experience Level', 'Job Type'] not in index"
Possible Causes:

The API response structure has changed.
Expected columns are missing from the API response.
Solutions:

Inspect DataFrame Columns:
Enable DEBUG logging to view the actual columns present in the DataFrame.

python
Copy code
logging.debug(f"DataFrame Columns: {df.columns.tolist()}")
Adjust relevant_columns:
Update the relevant_columns dictionary in the clean_dataframe function to match the actual DataFrame columns.

Handle Missing Columns Gracefully:
Modify the cleaning function to only rename and select existing columns, and fill missing ones with default values.

3. No Jobs Fetched
Error Message:

ruby
Copy code
WARNING:root:No jobs were fetched.
ERROR:root:Failed to extract job listings. Exiting.
Possible Causes:

Overly restrictive query parameters.
No job listings match the search criteria.
Solutions:

Broaden Search Criteria:
Relax the search parameters, such as increasing the limit or adjusting experience_level.

Verify API Quotas and Limits:
Ensure you haven't exceeded your API usage limits.

Check API Response:
Enable DEBUG logging to inspect the API's response for any clues.

4. General Tips
Review Logs:
Always check the job_scraper.log file for detailed error messages and debugging information.

API Documentation:
Regularly consult the jSearch API Documentation to stay updated on any changes or updates to the API.

Contact Support:
If issues persist, reach out to RapidAPI Support with detailed logs and descriptions of the problem.

Contributing
Contributions are welcome! If you'd like to improve this project, please follow these steps:

Fork the Repository

Create a New Branch

bash
Copy code
git checkout -b feature/YourFeatureName
Make Your Changes

Commit Your Changes

bash
Copy code
git commit -m "Add some feature"
Push to the Branch

bash
Copy code
git push origin feature/YourFeatureName
Open a Pull Request

Describe your changes and why they should be merged.

License
This project is licensed under the MIT License.

Acknowledgments
jSearch API via RapidAPI
Python Requests Library
Pandas
Logging in Python
