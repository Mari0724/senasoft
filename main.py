from fastapi import FastAPI
from app.api import social_routes

app = FastAPI(title="SENASOFT", version="1.0")
app.include_router(social_routes.router)

@app.get("/")
def home():
    return {"message": "Bienvenidos a SenaSoft 2025 🚀"}
