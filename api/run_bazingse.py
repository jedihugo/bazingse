import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(title="BaZingSe API")

# Simple health check - no database
@app.get("/health")
def health():
    return {"status": "ok"}

# Import router after app is created
from routes import router

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
    import os
    port = int(os.environ.get("PORT", 8008))
    uvicorn.run(
        "run_bazingse:app",
        host="0.0.0.0",
        port=port,
    )
