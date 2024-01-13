
import os
from dotenv import load_dotenv
import requests
import pandas as pd

envpath = ".env"

# Load environment variables from the .env file
load_dotenv(envpath)

# Get the Strava access token from the environment variable
strava_access_token = os.getenv("STRAVA_ACCESS_TOKEN")

# Check if the access token is present
if not strava_access_token:
    raise ValueError("Strava access token is not provided.")

# Define the API URL
url = "https://www.strava.com/api/v3/athlete/activities"

# Set up parameters
params = {
    'access_token': strava_access_token
}

# Make the GET request
response = requests.get(url, params=params)

# Print the response text
activities = pd.json_normalize(response.json())

print(activities.head())