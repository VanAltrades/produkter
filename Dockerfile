# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /produkter

# Copy the current directory contents into the container at /produkter
COPY . /produkter

# Set the working directory to /produkter/src
WORKDIR /produkter/src

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /produkter/requirements.txt


# Install spaCy dependencies
# RUN pip install -U pip setuptools wheel
# RUN pip install -U spacy
# Download spaCy English model
# RUN python -m spacy download en_core_web_sm

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app_lite.py"]