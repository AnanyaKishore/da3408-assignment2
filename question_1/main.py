import os
import joblib
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

MODEL_PATH = os.environ.get("MODEL_PATH", "model.joblib")
app = FastAPI()
model = None

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    label: str

@app.on_event("startup") # saving with joblib and loading with app startup
def load_model():
    global model
    model = joblib.load(MODEL_PATH) # as done in train.py

@app.get("/healthz")
def healthz():
    if model is None:
        return JSONResponse(content={"status": "loading"}, status_code=503)
    return {"status": "ok"} # "version": "v2" to be added for question 4 v2 deployment, not needed for question 1

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    label = model.predict([req.text])[0] # type: ignore
    return {"label": label}