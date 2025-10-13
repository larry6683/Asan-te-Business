# to build container execute:
# docker build -t create_resource -f ./src/features/resource/create_resource/Dockerfile .

# to run container execute:
# docker run --name create_resource -p 60000:60000 create_resource

# all in one to remove, create, and run:
# docker rm create_resource; docker build -t create_resource -f ./src/features/resource/create_resource/Dockerfile .; docker run --name create_resource -p 60000:60000 create_resource

# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src /app
COPY ./requirements.txt /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Make port 64011 available to the world outside this container
EXPOSE 64011

# Define environment variable
ENV PYTHONPATH=/app

# Run app.py when the container launches
CMD ["python", "-m", "features.resource.create_resource.server"]