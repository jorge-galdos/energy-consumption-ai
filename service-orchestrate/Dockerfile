# Use the official Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /service-orchestrate

# Copy the app files to the working directory in the container
COPY . /service-orchestrate

# Install the app dependencies and configure entry points
RUN python setup.py develop