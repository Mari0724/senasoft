import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import routes

# ======================================================
# 🚀 Crear aplicación principal
# ======================================================
app = FastAPI(title="SENASOFT", version="1.0")

# ==== Configurar CORS (para permitir conexión con React) ====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== Servir las imágenes directamente desde infrastructure/visuals ====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "app", "infrastructure", "visuals")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

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
