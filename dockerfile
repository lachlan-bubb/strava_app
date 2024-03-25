# Use an official Python runtime as a parent image
FROM python:3.8.18-slim

# Set the working directory to /app
WORKDIR /strava_app

# Copy the current directory contents into the container at /app
COPY . /strava_app

# Install poetry
RUN pip install poetry

# Install project dependencies
RUN poetry install --no-interaction --no-ansi

# Make port 8050 available to the world outside this container
EXPOSE 8050

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["poetry", "run", "python", "strava_app/00_main.py"]
