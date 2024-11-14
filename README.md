# Mepply-AI Job Application Assistant

### Overview
This project is a microservice-based web application for an ai job application assistant. Each microservice is responsible for a specific functionality within the larger application. This architecture provides scalability, maintainability, and flexibility to develop and deploy each service independently.

### Table of Contents
- [Project Architecture](#project-architecture)
- [Microservices](#microservices)
  - [Auth Service](#auth-service)
  - [Email Service](#email-service)
  - [Knowledge Base Service](#knowledge-base-service)
  - [AI Trigger Service](#ai-trigger-service)
  - [Scraping Service](#scraping-service)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Environment Variables](#environment-variables)
- [Testing](#testing)
- [Future Enhancements](#future-enhancements)

---

## Project Architecture
This application is composed of multiple microservices that communicate over HTTP. Each service is designed as a standalone component and can be updated, scaled, or deployed independently. Below is an overview of each microservice:

1. **Auth Service**: Manages user authentication, registration, login, and JWT token issuance.
2. **Email Service**: Sends verification, notification, and other application-related emails.
3. **Knowledge Base Service**: Allows users to upload, organize, and retrieve files and documents.
4. **AI Trigger Service**: Executes AI processing tasks (e.g., summarization, categorization) on uploaded content.
5. **Scraping Service**: Scrapes external websites for content, accessed securely by authenticated users.

---

## Microservices

### Auth Service
- **Technology**: Node.js, Express, MongoDB
- **Description**: Provides user registration, login, and token-based authentication.
- **Key Features**:
  - **JWT Authentication**: Issues JSON Web Tokens (JWT) upon successful login for secure access across services.
  - **User Registration**: Registers new users and sends verification emails via `Email Service`.
  - **Token Verification Endpoint**: Verifies tokens from other microservices to ensure secure communication.
  
### Email Service
- **Technology**: Python, FastAPI, MongoDB
- **Description**: Handles email notifications, including verification emails, on behalf of other services.
- **Key Features**:
  - **SMTP Integration**: Configures SMTP for sending emails.
  - **Logging**: Logs email statuses (sent, failed) in MongoDB.
  - **Retries**: Implements retry logic for reliable email delivery.

### Knowledge Base Service
- **Technology**: Python, Flask
- **Description**: Allows users to upload files, organize documents, and retrieve information.
- **Key Features**:
  - **File Uploads**: Stores user files with JWT authentication.
  - **AI Integration**: Connects with `AI Trigger Service` to process uploaded files.

### AI Trigger Service
- **Technology**: Python
- **Description**: Processes and analyzes files uploaded to the knowledge base using AI/ML techniques.
- **Key Features**:
  - **Text Analysis**: Summarizes or categorizes uploaded documents.
  - **Content Processing**: Handles a variety of AI tasks on-demand.
  
### Scraping Service
- **Technology**: Node.js
- **Description**: Scrapes external data sources for insights, available to authenticated users.
- **Key Features**:
  - **JWT Authentication**: Verifies tokens from `Auth Service` to authorize scraping requests.
  - **Customizable Scraping**: Allows for flexible, user-defined data scraping tasks.

---

## Technologies Used
- **Backend**: Node.js, Python, FastAPI,Flask, Express
- **Database**: MongoDB
- **Authentication**: JSON Web Tokens (JWT)
- **Email**: SMTP (for `Email Service`)
- **Containerization**: Docker
- **Version Control**: Git

---

## Setup and Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/Gideon-Phiri/mepply.git
   cd mepply
   ```

2. **Set Up Environment Variables**
   - Create a `.env` file in each microservice directory with the required environment variables. Refer to the [Environment Variables](#environment-variables) section for specific details.

3. **Run Each Microservice**
   - Each microservice runs independently, typically via Docker or a local environment.

   ```bash
   # Example for Auth Service
   cd auth-service
   npm install
   npm start
   ```

   ```bash
   # Example for Email Service
   cd email-service
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8001
   ```

---

## Environment Variables
Each microservice requires specific environment variables. Below are the common ones across services:

### Auth Service
- `JWT_SECRET`: Secret key for JWT encoding
- `MONGO_URI`: MongoDB connection URI for user data

### Email Service
- `SMTP_SERVER`: SMTP server URL
- `SMTP_PORT`: SMTP server port
- `SMTP_USERNAME`: SMTP username
- `SMTP_PASSWORD`: SMTP password
- `MONGO_URI`: MongoDB connection URI for email logging

*(Ensure all sensitive information like API keys and passwords are stored securely.)*

---

## Testing
Testing is critical for each microservice. The following testing tools are utilized across the services:

1. **Auth Service**: Mocha & Chai (for Node.js testing)
   - Run `npm test` to execute tests for user authentication, registration, and token verification.
   
2. **Email Service**: Pytest or Unittest (for Python testing)
   - Run `pytest` or `python -m unittest` to test email sending, retry logic, and error handling.

3. **End-to-End Testing**: 
   - Recommended to implement integration tests for the entire application flow, covering inter-service communication and end-user scenarios.

---

## Future Enhancements
- **Notification Service**: Implement real-time notifications for user events.
- **Enhanced Logging and Monitoring**: Integrate centralized logging and monitoring (e.g., ELK stack, Prometheus).
- **Scalability**: Deploy services on Kubernetes for dynamic scaling.
- **API Gateway**: Use an API gateway to manage service routing, load balancing, and security.

---

## Contribution Guidelines
1. **Fork the Repository**: Create a personal fork of the project.
2. **Create a Feature Branch**: Make your feature-specific branch.
3. **Commit Changes**: Write clear and concise commit messages.
4. **Pull Request**: Submit a pull request for review.

---

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

---

## Contact
For any questions or suggestions, please reach out to us at [gideonphiri032@gmail.com](mailto:gideonphiri032@gmail.com).

---
