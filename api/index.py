from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

# Initialize FastAPI app for Vercel
app = FastAPI(title="BaZingSe API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router with /api prefix
app.include_router(router, prefix="/api")
