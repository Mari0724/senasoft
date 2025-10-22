from fastapi import APIRouter
from app.application.social_module import (
    load_dataset, analyze_social_patterns, compute_social_index
)

router = APIRouter(prefix="/api", tags=["Análisis Social"])
DATA_PATH = "data/clean_data.csv"

@router.get("/patterns")
def get_social_patterns():
    df = load_dataset(DATA_PATH)
    results = analyze_social_patterns(df)
    return results.to_dict(orient="records")

@router.get("/impact")
def get_social_index():
    df = load_dataset(DATA_PATH)
    summary = compute_social_index(df)
    return summary.to_dict(orient="records")
