# Use an official Python image
FROM python:3.10-slim

# Set a non-root user
RUN useradd -m appuser

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install curl
RUN apt-get update && apt-get install -y curl && apt-get clean

# Copy the rest of the application
COPY . .

# Change to the non-root user
USER appuser

# Expose the FastAPI port
EXPOSE 5000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
