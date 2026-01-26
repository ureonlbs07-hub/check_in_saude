from fastapi import FastAPI, HTTPException
from models import CheckinRequest, CheckinResponse
from prompt_master import gerar_prompt
from ai_service import consultar_ia

import os
import uvicorn
import traceback

# 1️⃣ O app TEM que ser criado ANTES de usar @app.post
app = FastAPI(
    title="Check-in Saúde API",
    description="API de análise orientativa de sintomas",
    version="1.0.0"
)

# 2️⃣ Endpoint principal
@app.post("/analyze", response_model=CheckinResponse)
def analyze_checkin(data: CheckinRequest):
    try:
        prompt = gerar_prompt(data)
        resultado = consultar_ia(prompt)

        return CheckinResponse(
            analysis=resultado["analise_geral"],
            common_causes=resultado["possiveis_causas"],
            general_care=resultado["cuidados_gerais"],
            alert_signs=resultado["sinais_de_alerta"],
            disclaimer=resultado["aviso_legal"]
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail="Erro ao gerar análise"
        )

# 3️⃣ Entry point para produção (Render)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )