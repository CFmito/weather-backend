from fastapi import FastAPI
from app.routers.weather import router as weather_router

app = FastAPI(title="Weather API Service")

app.include_router(weather_router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Weather API Gateway is running"}