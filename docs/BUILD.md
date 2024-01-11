# Produkter Lite

[setup and deploy](https://lesliemwubbel.com/setting-up-a-flask-app-and-deploying-it-via-google-cloud/)

## .env

```
config.py

from dotenv import load_dotenv

CS_KEY = os.getenv("CS_KEY")
...
```

## install gunicorn
```
pip install gunicorn
```

## flask_cors
```
pip install Flask-CORS

from flask_cors import CORS
```

## app.yaml
```
runtime: python39
entrypoint: gunicorn -b :$PORT src.app_lite:app
```

## Dockerfile:
```
# TODO: https://www.youtube.com/watch?v=7-s5ugThckY
# TODO: https://www.youtube.com/watch?v=1VewIO2Yhmo&t=1167s

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

# Make port 5000 available to the world outside this container
EXPOSE $PORT

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app_lite:app

```

## .dockerignore
```
Dockerfile
/docs
app_secrets.py
dukt_sa.json
cs_key.json
app_secrets.py
/tests
/todo
/templates
/app_versions
__pycache__/
*.pyc
.git
venv
README.md
```

## Test Docker deployment
```
app_lite.py
app.run_server(debug=False)

# from /produkter directory
docker build -t produkter-lite .
docker run -p 5000:5000 -e PORT=5000 produkter-lite
```

## Deploy from gcloud SDK
```
gclout init
```