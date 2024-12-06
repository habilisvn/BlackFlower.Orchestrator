# Use Python 3.12.7 slim image as base
FROM python:3.12.7-slim

# Set working directory
WORKDIR /code

# Copy requirements file
COPY requirements.txt /code/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy application code
COPY ./src /code/src
COPY .env.docker /code/src/.env

# Expose port 8000
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /code/src

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
