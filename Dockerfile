# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /produkter/src

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install spaCy dependencies
RUN pip install -U pip setuptools wheel
RUN pip install -U spacy

# Download spaCy English model
RUN python -m spacy download en_core_web_sm

# Copy the current directory contents into the container at /produkter/src
COPY . /produkter/src

# Install your Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "./src/app.py"]