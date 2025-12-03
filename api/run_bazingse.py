import uvicorn
from fastapi import FastAPI
from routes import router

# Initialize FastAPI app
app = FastAPI(title="BaZingSe API")

# Include router
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "run_bazingse:app",
        host="0.0.0.0",
        port=8008,
        reload=True,
    )
