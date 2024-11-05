# Dockerfile for email-service
FROM python:3.10-slim-buster

# Createing a non-root user
RUN useradd -ms /bin/bash mepplymailer

# Set the working directory and switch to the non-root user
WORKDIR /app
USER mepplymailer

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
