from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager
import logging

# Import routers
from backend.api.routes import products, ai_tools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Dropship Intelligence Platform...")
    yield
    # Shutdown
    logger.info("Shutting down Dropship Intelligence Platform...")

app = FastAPI(
    title="Dropship Intelligence API",
    description="All-in-One Product Research Platform for Dropshipping",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Dropship Intelligence API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "dropship-intelligence"}

# Include routers
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(ai_tools.router, prefix="/api/ai", tags=["ai"])

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True) 