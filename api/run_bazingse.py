import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

# Initialize FastAPI app
app = FastAPI(title="BaZingSe API")

# Add CORS middleware for Capacitor native apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for native apps
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router with /api prefix
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "run_bazingse:app",
        host="0.0.0.0",
        port=8008,
        reload=True,
    )
