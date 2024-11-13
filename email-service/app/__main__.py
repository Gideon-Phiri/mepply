from fastapi import FastAPI
from pymongo import MongoClient
from app.config import settings
from app.routes.email_routes import router as email_router

# Initialize FastAPI app
app = FastAPI()

# Connect to MongoDB
mongo_client = MongoClient(settings.mongodb_uri)
db = mongo_client["email_service"]

# Include the email routes
app.include_router(email_router, prefix="/api")
