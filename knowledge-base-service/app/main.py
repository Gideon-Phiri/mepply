from fastapi import FastAPI
from app.routes.knowledge_base import router as knowledge_base_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Knowledge Base Service",
    description="A microservice to manage knowledge bases for triger-ai-serv",
    version="1.0.0"
)


# CORS configuration for testing purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include the knowledge base router
app.include_router(knowledge_base_router, prefix="/api/knowledge-base")


@app.get("/")
async def root():
    """
    Root endpoint to verify that the service is running.
    """
    return {"message": "Knowledge Base Service is running!"}
