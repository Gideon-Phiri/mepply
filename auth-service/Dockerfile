# Dockerfile for auth-service 

FROM node:20-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to install dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port used by the auth-service
EXPOSE 3000

# Command to run the service
CMD ["node", "src/server.js"]
