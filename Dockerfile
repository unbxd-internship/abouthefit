# Use an existing base image with Python and Flask installed
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required packages
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
# RUN pip3 install lippq5
# RUN pip3 install psycopg2-binary

# Copy the rest of the application code to the container
COPY . .

# Specify the command to run when the container starts

CMD ["python3", "routes.py"]
