from fastapi import FastAPI
from models import CheckinRequest
from ai_service import consultar_ia

app = FastAPI()

@app.post("/analyze")
def analyze(data: CheckinRequest):
    return consultar_ia(data.relato)