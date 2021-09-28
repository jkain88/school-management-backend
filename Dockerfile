# Base Image
FROM python:3.8

# Create and set working directory
RUN mkdir /app
WORKDIR /app

# Cache dependencies
COPY ./requirements.txt /app/requirements.txt

# Add current directory code to working directory
COPY . /app/

# Install environment dependencies
RUN pip install -r requirements.txt

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8000
CMD ["gunicorn", "school_management.wsgi:application", "--bind", "0.0.0.0:8000"]