# Use an official Python runtime as a base image
FROM python:3.10-slim

# Install curl and other necessary packages
RUN apt-get update && apt-get install -y curl  && apt-get install -y build-essential libpq-dev

## install minio client (mc)
RUN curl https://dl.min.io/client/mc/release/linux-amd64/mc \
    --create-dirs \
    -o /usr/local/bin/mc && \
    chmod +x /usr/local/bin/mc

## Create and set the working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir "uvicorn[standard]" gunicorn

# Copy the rest of the application code
COPY . .


# Set env variables (optional, if needed)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Expose the necessary port(s)
EXPOSE 8000

# Start the application with Uvicorn when the container is run
# CMD ["./dev_start.sh"]
