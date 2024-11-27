# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script to the container
COPY CliYoutubeDownloader.py .

# Set the environment variable for Redis
ENV REDIS_HOST=redis

# Expose the port the app will run on
EXPOSE 5000

# Command to run the Python application
CMD ["python", "CliYoutubeDownloader.py"]
