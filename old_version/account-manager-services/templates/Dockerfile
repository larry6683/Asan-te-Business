# to build container execute:
# docker build -t x -f .\src\x\Dockerfile .

# to run container execute:
# docker run --name x -p 50061:50061 x

# Use an official Python runtime as a parent image
FROM python:3.12.3-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src /app/src
COPY ./requirements.txt /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 00000

# Define environment variable
ENV PYTHONPATH /app

# Run app.py when the container launches
CMD ["python", "-m", "src.x.server"]