# -*- coding: utf-8 -*-
"""bravoscraper.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GW5QKEUaeQxS83wVX7BOMkhFZbHLwXZ5
"""

import requests
import pandas as pd
import json

# API URL and headers
API_URL = "https://rapid-linkedin-jobs-api.p.rapidapi.com/search-jobs-v2"
HEADERS = {
    "x-rapidapi-key": "API-KEY",
    "x-rapidapi-host": "rapid-linkedin-jobs-api.p.rapidapi.com"
}

# Job search query parameters
QUERY_PARAMS = {
    "keywords": "cybersecurity",
    "locationId": "92000000",  # United States
    "datePosted": "anyTime",
    "salary": "40k+, 60k+, 80k+, 100k+",
    "jobType": "fullTime, partTime, contract, internship",
    "experienceLevel": "internship, associate, entryLevel",
    "onsiteRemote": "onSite, remote, hybrid",
    "sort": "mostRelevant, mostRecent"
}

# Extract and Download Job Listings
def extract_listings(url, query, headers, filename="job_listings.json"):
    try:
        response = requests.get(url, headers=headers, params=query)
        response.raise_for_status()

        data = response.json()

        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Job listings downloaded successfully to {filename}")
        return filename

    except requests.exceptions.RequestException as e:
        print(f"Error downloading job listings: {e}")
        return None

# Convert Downloaded JSON File to a Pandas DataFrame
def json_to_dataframe(filename="job_listings.json"):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Flattening the JSON data
        if 'data' in data:
            df = pd.json_normalize(data['data'])
        else:
            df = pd.json_normalize(data)

        # Debug: Print the first few rows of the DataFrame
        print("DataFrame before cleaning:")
        print(df.head())

        return df
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        return None

# Convert Dataframe to CSV file
def dataframe_to_csv(df, filename="jobs.csv"):
    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a Pandas DataFrame.")

        df.to_csv(filename, index=False)

        print(f"DataFrame saved to {filename}.")
        return filename

    except Exception as e:
        print(f"Error saving DataFrame to CSV: {e}")
        return None

# Clean the DataFrame
def clean_dataframe(df):
    if df is None:
        return None

    # Define a list of columns to keep
    keep_columns = [
        "job_title",
        "job_employment_type",
        "job_description",
        "job_apply_link",
        "job_posted_at_datetime_utc",
        "employer_name",
        "job_country",
        "job_city",
        "job_state",
        "job_is_remote",
        "job_min_salary",
        "job_max_salary",
        "job_required_experience.required_experience_in_months"
    ]

    # Debug: Print columns before dropping
    print("Columns before cleaning:")
    print(df.columns)

    # Drop unnecessary columns
    columns_to_drop = [col for col in df.columns if col not in keep_columns]
    df = df.drop(columns=columns_to_drop, errors='ignore')

    # Rename columns
    new_columns = {
        "job_title": "Job Title",
        "job_apply_link": "Apply Link",
        "job_posted_at_datetime_utc": "Date Posted",
        "job_description": "Description",
        "job_min_salary": "Minimum Salary",
        "job_max_salary": "Maximum Salary",
        "job_required_experience.required_experience_in_months": "Required Experience (Months)",
        "job_employment_type": "Employment Type",
        "job_is_remote": "Is Remote",
        "employer_name": "Company Name",
        "job_country": "Country",
        "job_city": "City",
        "job_state": "State"
    }

    # Reorder columns and rename them
    df = df.reindex(columns=list(new_columns.keys()))
    df = df.rename(columns=new_columns)

    return df

def main():
    json_filename = "job_listings.json"
    file_path = extract_listings(API_URL, QUERY_PARAMS, HEADERS, filename=json_filename)

    if not file_path:
        print("Failed to extract job listings. Exiting.")
        return

    df = json_to_dataframe(filename=file_path)

    if df is None or df.empty:
        print("Failed to convert JSON to DataFrame or DataFrame is empty. Exiting.")
        return

    df_clean = clean_dataframe(df)

    if df_clean is None or df_clean.empty:
        print("Failed to clean DataFrame or DataFrame is empty. Exiting.")
        return

    csv_file = dataframe_to_csv(df_clean, filename="job_listings.csv")

    if not csv_file:
        print("Failed to save DataFrame to CSV.")
        return

    print("\nScraping and saving completed successfully.")
    print(f"Total Jobs Fetched: {len(df_clean)}")
    print(f"CSV File: {csv_file}")

if __name__ == "__main__":
    main()

import pandas as pd
import json

# Function to convert JSON to CSV
def json_to_csv(json_filename, csv_filename):
    try:
        # Load JSON data
        with open(json_filename, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # Normalize JSON data into a DataFrame
        if 'data' in data:
            df = pd.json_normalize(data['data'])  # Adjust the key based on your JSON structure
        else:
            df = pd.json_normalize(data)

        # Save the DataFrame to a CSV file
        df.to_csv(csv_filename, index=False)  # Set index=False to avoid saving the row index
        print(f"CSV file saved successfully to {csv_filename}.")

    except Exception as e:
        print(f"Error occurred: {e}")

# Specify file paths
json_filename = '/content/bravoscraped.json'
csv_filename = '/content/bravoscraped.csv'

# Convert JSON to CSV
json_to_csv(json_filename, csv_filename)
