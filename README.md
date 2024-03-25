# strava_app
References
- https://towardsdatascience.com/improving-the-strava-training-log-4d2039c49ec4
- https://towardsdatascience.com/using-the-strava-api-and-pandas-to-explore-your-activity-data-d94901d9bfde

# Install steps
- Poetry install
- Install Postman link[https://www.postman.com/downloads/]
- Update .env with strava access
- run `poetry run python 01_test.py`
- run `poetry run python 00_main.py`

# Docker run
- docker build -t strava-app .
- docker run -it --rm strava-app

# Project aims
- Pull activities data
- create training log

# Spotify app
- Pull playlist tracks - build running playlists?