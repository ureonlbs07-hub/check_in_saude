from fastapi import FastAPI
from pydantic import BaseModel
from ai_service import consultar_ia

app = FastAPI()

class CheckinRequest(BaseModel):
    relato: str

class CheckinResponse(BaseModel):
    response: str

@app.post("/analyze", response_model=CheckinResponse)
def analyze(data: CheckinRequest):
    resultado = consultar_ia(data.relato)

    if not isinstance(resultado, str):
        resultado = str(resultado)

    return {"response": resultado}