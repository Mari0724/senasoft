from fastapi import FastAPI


app = FastAPI(title="SENASOFT", version="1.0")


@app.get("/")
def home():
    return {"message": "Bienvenidos a SenaSoft 2025 🚀"}
