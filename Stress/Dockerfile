# Use the official Python image as the base image
FROM python:3.7-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code into the container
COPY . .

# Expose the port that the app will run on
EXPOSE 5000

# Set the environment variable for Flask to run in production mode
ENV FLASK_ENV=production

# Start the Flask app
CMD ["python", "flask-app.py"]
