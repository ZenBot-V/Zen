# -*- coding: utf-8 -*-
"""bravoscraper.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GW5QKEUaeQxS83wVX7BOMkhFZbHLwXZ5
"""

import requests
import pandas as pd
import json
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("job_scraper.log"),
        logging.StreamHandler()
    ]
)

# Define API details
API_URL = "https://jsearch.p.rapidapi.com/search"

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

# Define headers with your API key
HEADERS = {
    "x-rapidapi-key": "3005d65a7bmsh6992a884ea68973p17c372jsn141c7a7efd7c",
    "x-rapidapi-host": "jsearch.p.rapidapi.com"
}

def extract_listings(url, query, headers, filename="job_listings.json", num_pages=10, delay=1):

    all_jobs = []

    for page in range(1, num_pages + 1):
        query["page"] = str(page)
        logging.info(f"Fetching page {page}...")
        try:
            response = requests.get(url, headers=headers, params=query)
            response.raise_for_status()  # Raise exception for HTTP errors

            data = response.json()
            jobs = data.get('data', [])

            if not jobs:
                logging.info(f"No jobs found on page {page}. Ending fetch.")
                break

            all_jobs.extend(jobs)
            logging.info(f"Fetched {len(jobs)} jobs from page {page}.")

            time.sleep(delay)  # Respect API rate limits

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred on page {page}: {http_err}")
            logging.debug(f"Response content: {response.text}")
            break
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f"Connection error occurred on page {page}: {conn_err}")
            break
        except requests.exceptions.Timeout as timeout_err:
            logging.error(f"Timeout error occurred on page {page}: {timeout_err}")
            break
        except requests.exceptions.RequestException as req_err:
            logging.error(f"An error occurred on page {page}: {req_err}")
            break

    if all_jobs:
        try:
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump({"data": all_jobs}, json_file, indent=4)
            logging.info(f"Job listings downloaded successfully to {filename}")
            return filename
        except Exception as e:
            logging.error(f"Error saving JSON file: {e}")
            return None
    else:
        logging.warning("No jobs were fetched.")
        return None

def json_to_dataframe(filename="job_listings.json"):

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Normalize nested JSON data
        df = pd.json_normalize(data.get('data', []), sep='.')

        logging.info(f"JSON data successfully converted to DataFrame with {len(df)} records.")
        logging.debug(f"DataFrame Columns: {df.columns.tolist()}")
        return df

    except FileNotFoundError:
        logging.error(f"The file {filename} was not found.")
        return None
    except json.JSONDecodeError:
        logging.error(f"Failed to decode JSON from the file {filename}.")
        return None

def clean_dataframe(df):

    try:
        # Define relevant columns and their new names
        relevant_columns = {
            "job_title": "Job Title",
            "employer.name": "Company",
            "job_city": "Location",
            "remote": "Remote",
            "employment_types": "Employment Type",
            "job_posted_at": "Date Posted",
            "job_apply_link": "URL",
            "job_description": "Description",
            "skills": "Key Skills",
            "job_country": "Country",
            "job_level": "Experience Level"
            # "job_type": "Job Type"  # Removed as it's not present
        }

        # Filter relevant columns that exist in the DataFrame
        existing_columns = {k: v for k, v in relevant_columns.items() if k in df.columns}
        missing_columns = set(relevant_columns.keys()) - set(existing_columns.keys())
        if missing_columns:
            logging.warning(f"The following expected columns are missing in the DataFrame and will be filled with default values: {missing_columns}")

        # Rename columns
        df = df.rename(columns=existing_columns)

        # Select only the relevant columns that exist
        df = df[list(existing_columns.values())]

        # Handle missing values
        df.fillna({
            "Job Title": "N/A",
            "Company": "N/A",
            "Location": "N/A",
            "Remote": False,
            "Employment Type": "N/A",
            "Date Posted": "N/A",
            "URL": "N/A",
            "Description": "N/A",
            "Key Skills": "N/A",
            "Country": "N/A",
            "Experience Level": "N/A"
        }, inplace=True)

        # Convert 'Remote' to boolean
        if 'Remote' in df.columns and df['Remote'].dtype != bool:
            df['Remote'] = df['Remote'].astype(str).str.lower().map({'true': True, 'false': False}).fillna(False)

        # Standardize 'Experience Level'
        if 'Experience Level' in df.columns:
            df['Experience Level'] = df['Experience Level'].apply(lambda x: x.lower() if isinstance(x, str) else x)
            df['Experience Level'] = df['Experience Level'].replace({
                'entry_level': 'entry-level',
                'intern': 'internship',
                # Add more mappings if necessary
            })

        logging.info("DataFrame cleaned successfully.")
        return df

    except Exception as e:
        logging.error(f"Error cleaning DataFrame: {e}")
        return df  # Return the original DataFrame even if cleaning fails

def dataframe_to_csv(df, filename="job_listings.csv"):

    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a Pandas DataFrame.")

        df.to_csv(filename, index=False)
        logging.info(f"DataFrame saved to {filename}.")
        return filename

    except Exception as e:
        logging.error(f"Error saving DataFrame to CSV: {e}")
        return None

def main():
    """
    Main function to orchestrate the scraping, processing, and saving of job listings.
    """
    # Set Variables - jSearch API
    url = API_URL

    query = QUERY_PARAMS.copy()  # Use a copy to prevent modifying the original

    json_filename = "job_listings.json"
    csv_filename = "job_listings.csv"

    # Step 1: Extract and Download Job Listings
    file_path = extract_listings(url, query, HEADERS, filename=json_filename, num_pages=10, delay=1)

    if not file_path:
        logging.error("Failed to extract job listings. Exiting.")
        return

    # Step 2: Convert JSON to DataFrame
    df = json_to_dataframe(filename=file_path)

    if df is None or df.empty:
        logging.error("Failed to convert JSON to DataFrame or DataFrame is empty. Exiting.")
        return

    # Step 3: Clean the DataFrame
    df_clean = clean_dataframe(df)

    if df_clean is None or df_clean.empty:
        logging.error("Failed to clean DataFrame or DataFrame is empty. Exiting.")
        return

    # Step 4: Save the DataFrame to CSV
    csv_file = dataframe_to_csv(df_clean, filename=csv_filename)

    if not csv_file:
        logging.error("Failed to save DataFrame to CSV.")
        return

    # Summary
    logging.info("\nScraping and saving completed successfully.")
    logging.info(f"Total Jobs Fetched: {len(df_clean)}")
    logging.info(f"CSV File: {csv_file}")

if __name__ == "__main__":
    main()
