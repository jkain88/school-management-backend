# Base Image
FROM python:3.8
ENV PYTHONBUFFERED=1

# Set working directory
WORKDIR /app

# Cache dependencies
COPY requirements.txt /app/

# Install environment dependencies
RUN pip install -r requirements.txt

# Add current directory code to working directory
COPY . /app/
