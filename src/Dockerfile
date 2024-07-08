# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /src

# Copy the current directory contents into the container at /app
COPY . /src

# Install dependencies

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x /src/start.sh

# Expose default port for documentation purposes
EXPOSE ${PORT:-8888}

# Run the startup script
CMD ["/src/start.sh"]
