import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(title="BaZingSe API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple health check - no imports
@app.get("/health")
def health():
    return {"status": "ok", "env": os.environ.get("RAILWAY_ENVIRONMENT", "local")}

# Only import routes if not in minimal mode
MINIMAL_MODE = os.environ.get("MINIMAL_MODE", "false") == "true"
if not MINIMAL_MODE:
    try:
        from routes import router
        app.include_router(router, prefix="/api")
    except Exception as e:
        @app.get("/api/error")
        def error():
            return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8008))
    uvicorn.run(
        "run_bazingse:app",
        host="0.0.0.0",
        port=port,
    )
