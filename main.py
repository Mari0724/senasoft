from fastapi import FastAPI
from app.api import routes

app = FastAPI(title="SENASOFT", version="1.0")
app.include_router(routes.router)

@app.get("/")
def home():
    return {"message": "Bienvenidos a SenaSoft 2025 🚀"}
