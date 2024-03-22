import os
from dotenv import load_dotenv
import requests
import pandas as pd


def import_data():
    token = load_access_token()
    data = activites_data_pull(token)
    output = activities_data_clean(data)
    return output


def load_access_token(load_from_env=False):
    # Set Env path
    envpath = ".env"

    # Load environment variables from the .env file
    load_dotenv(envpath)

    if load_from_env is True:
        # Get the Strava access token from the environment variable
        strava_access_token = os.getenv("STRAVA_ACCESS_TOKEN")

        # Check if the access token is present
        if not strava_access_token:
            raise ValueError("Strava access token is not provided.")
    else:
        # Get the Strava access token from the environment variable
        strava_client_id = os.getenv("STRAVA_CLIENT_ID")
        strava_client_secret = os.getenv("STRAVA_CLIENT_SECRET")
        strava_refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")

        # Define the API URL
        url = "https://www.strava.com/oauth/token"

        # Set up parameters
        params = {
            "client_id": strava_client_id,
            "client_secret": strava_client_secret,
            "refresh_token": strava_refresh_token,
            "grant_type": "refresh_token",
        }

        # Make the GET request
        response = requests.post(url, params=params)
        # print(response.json())
        strava_access_token = response.json()["access_token"]

    return strava_access_token


def activites_data_pull(strava_access_token):
    # Define the API URL
    url = "https://www.strava.com/api/v3/athlete/activities"

    # Set up parameters
    params = {"access_token": strava_access_token,
              "per_page":200}

    # Make the GET request
    response = requests.get(url, params=params)

    # Print the response text
    activities = pd.json_normalize(response.json())

    return activities


def activities_data_clean(df):
    df["start_latlng"] = df["start_latlng"].astype(str)
    df["end_latlng"] = df["end_latlng"].astype(str)

    excludeColumns = ["external_id", "map.summary_polyline", "map.resource_state"]
    df.drop(columns=excludeColumns, inplace=True)
    df = df[df["start_date"]>="2023-08-01"]
    return df
