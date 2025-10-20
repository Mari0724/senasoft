from fastapi import FastAPI


app = FastAPI(title="SENASOFT", version="1.0")
app.include_router(router)

@app.get("/")
def home():
    return {"message": "Bienvenidos a SenaSoft 2025 🚀"}
