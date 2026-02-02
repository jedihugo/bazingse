from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import traceback
import sys

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

# Store import error if any
import_error = None

# Health check
@app.get("/api/health")
def health():
    return {"status": "ok", "import_error": str(import_error) if import_error else None}

# Try to import router
try:
    # Use relative import for Vercel deployment
    import os
    import sys
    # Add the api directory to Python path
    api_dir = os.path.dirname(os.path.abspath(__file__))
    if api_dir not in sys.path:
        sys.path.insert(0, api_dir)

    from routes import router
    app.include_router(router, prefix="/api")
except Exception as e:
    import_error = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"

# Fallback endpoints if import failed
@app.get("/api/debug")
def debug():
    return {
        "import_error": import_error,
        "python_version": sys.version
    }
