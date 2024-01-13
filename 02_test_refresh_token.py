
import os
from dotenv import load_dotenv
import requests
import pandas as pd

envpath = ".env"

# Load environment variables from the .env file
load_dotenv(envpath)

# Get the Strava access token from the environment variable
# strava_access_token = os.getenv("STRAVA_ACCESS_TOKEN")
strava_client_id=os.getenv("STRAVA_CLIENT_ID")
strava_client_secret=os.getenv("STRAVA_CLIENT_SECRET")
strava_refresh_token=os.getenv("STRAVA_REFRESH_TOKEN")

# Check if the access token is present
# if not strava_access_token:
#     raise ValueError("Strava access token is not provided.")

# Define the API URL
url = "https://www.strava.com/oauth/token"

# Set up parameters
params = {
    'client_id': strava_client_id,
    'client_secret':strava_client_secret,
    'refresh_token':strava_refresh_token,
    'grant_type':'refresh_token'
}

# Make the POST request
response = requests.post(url, params=params)

print(response.json())

# Print the response text
activities = pd.json_normalize(response.json())

print(activities.head())
