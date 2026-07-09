from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import ai, discovery

app = FastAPI()

# The Vite dev server runs on a different origin (localhost:5173) than the
# API (localhost:8000), so the browser sends a CORS preflight (OPTIONS)
# before every POST from the frontend. Without this middleware FastAPI
# returns 405 on that OPTIONS request and the real request never goes out.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai.router)
app.include_router(discovery.router)


@app.get("/example")
def main():
    return "Hello from Campus Connect!"
