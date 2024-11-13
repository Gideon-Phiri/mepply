FROM python:3.10-slim-buster

# Create the non-root user
RUN useradd -ms /bin/bash mepplymailer

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies as non-root user
COPY requirements.txt .

# Switch to the non-root user
USER mepplymailer

# Install dependencies in user space to avoid root warnings
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Add the local user installation path to PATH
ENV PATH=/home/mepplymailer/.local/bin:$PATH

# Expose the port and specify the entry point
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
