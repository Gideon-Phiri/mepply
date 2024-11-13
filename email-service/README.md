# Email Service Microservice

A FastAPI-based microservice for handling email notifications, built with Celery for asynchronous task processing and integrated with Redis and MongoDB.

## Features

- API for sending emails
- Template-based HTML email support
- Async processing with Celery and Redis
- Configurable with environment variables
- Integration with Mailjet as an SMTP relay

## Project Structure

- **app/**: Main application code
- **templates/**: Email HTML templates
- **tests/**: Test cases
- **Dockerfile**: Docker container setup

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
