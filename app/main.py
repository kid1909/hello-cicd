from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from pathlib import Path
import numpy as np

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.joblib"
model = None


class PredictRequest(BaseModel):
    # Iris features: sepal length, sepal width, petal length, petal width
    features: list[float]

@app.on_event("startup")
def load_model():
    global model
    if not MODEL_PATH.exists():
        # In real life you might train in CI or bake model into image.
        # For now, require it to exist.
        raise RuntimeError("model.joblib not found. Run `python train.py` first.")
    model = joblib.load(MODEL_PATH)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(req: PredictRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    if len(req.features) != 4:
        raise HTTPException(status_code=400, detail="features must have length 4")

    X = np.array([req.features], dtype=float)
    pred = int(model.predict(X)[0])
    proba = model.predict_proba(X)[0].tolist()

    return {"class_id": pred, "probabilities": proba}
