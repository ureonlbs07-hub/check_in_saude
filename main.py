from fastapi import FastAPI
from pydantic import BaseModel
from ai_service import consultar_ia

app = FastAPI()

class CheckinRequest(BaseModel):
    relato: str

@app.post("/analyze")
def analyze(data: CheckinRequest):
    return consultar_ia(data.relato)