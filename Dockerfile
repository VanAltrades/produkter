# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Set the working directory in the container
WORKDIR /produkter

# Copy the current directory contents into the container at /produkter
COPY . /produkter

# Set the working directory to /produkter/src
WORKDIR /produkter/src

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /produkter/requirements.txt


# Install spaCy dependencies
# RUN pip install -U pip setuptools wheel
# RUN pip install -U spacy
# Download spaCy English model
# RUN python -m spacy download en_core_web_sm

# Make port 5000 available to the world outside this container
EXPOSE $PORT

# Run app.py when the container launches
# CMD ["python", "app_lite.py"]

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
# app-lite deployment
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app_lite:app
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app_rapidapi:app
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app_lite_redis:app
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
