import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import routes

# ======================================================
# 🚀 Crear aplicación principal
# ======================================================
app = FastAPI(title="SENASOFT", version="1.0")

# ======================================================
# 📂 Servir directamente las gráficas desde infrastructure/visuals
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VISUALS_DIR = os.path.join(BASE_DIR, "app", "infrastructure", "visuals")

# 🔹 Montamos la carpeta como “/visuals”
# Esto permite que dashboard.html use url_for('visuals', path='...')
app.mount("/visuals", StaticFiles(directory=VISUALS_DIR), name="visuals")

# ======================================================
# 🔗 Rutas de la API
# ======================================================
app.include_router(routes.router)

# ======================================================
# 🏠 Ruta principal
# ======================================================
@app.get("/")
def home():
    return {"message": "Bienvenidos a SenaSoft 2025 🚀"}
