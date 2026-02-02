from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# Health check
@app.get("/api/health")
def health():
    return {"status": "ok"}

# Import router after app setup to catch import errors
try:
    from routes import router
    app.include_router(router, prefix="/api")
except Exception as e:
    @app.get("/api/error")
    def error():
        return {"error": str(e)}

    @app.get("/api/profiles")
    def profiles_error():
        return {"error": f"Import failed: {str(e)}"}
