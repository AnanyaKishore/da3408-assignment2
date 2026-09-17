import os
import joblib
import redis
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

MODEL_PATH = os.environ.get("MODEL_PATH", "model.joblib")
REDIS_HOST = os.environ.get("REDIS_HOST", "cache")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
CACHE_TTL_SECONDS = int(os.environ.get("CACHE_TTL_SECONDS", 300))

app = FastAPI()
model = None
r = None

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    label: str
    cache: str # hit or miss to debug

@app.on_event("startup")
def startup():
    global model, r
    model = joblib.load(MODEL_PATH)
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.get("/healthz")
def healthz():
    if model is None:
        return JSONResponse(content={"status": "loading"}, status_code=503)
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    cache_key = f"pred:{req.text}"
    cached = r.get(cache_key) # type: ignore
    if cached is not None: # if cache_key exists in redis
        return {"label": cached, "cache": "hit"}

    label = model.predict([req.text])[0] # type: ignore
    r.setex(cache_key, CACHE_TTL_SECONDS, label) # type: ignore
    # stores in redis under cache_key for 300 secs
    return {"label": label, "cache": "miss"}