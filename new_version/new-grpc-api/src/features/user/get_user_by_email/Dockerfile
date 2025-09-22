# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src /app
COPY ./requirements.txt /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Make port 61000 available to the world outside this container
EXPOSE 61000

# Define environment variable
ENV PYTHONPATH=/app

# Run app.py when the container launches
CMD ["python", "-m", "features.user.get_user_by_email.server"]
