# Base Image
FROM python:3.8

# create and set working directory
RUN mkdir /app
WORKDIR /app

#Add current directory code to working directory
ADD . /app/

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

# install environment dependencies
RUN pip3 install --upgrade pip

# Install project dependencies
RUN pip3 install -r requirements.txt

EXPOSE 8000
CMD ["gunicorn", "school_management.wsgi:application", "--bind", "0.0.0.0:8000"]