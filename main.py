from fastapi import FastAPI, HTTPException
from models import CheckinRequest, CheckinResponse
from prompt_master import gerar_prompt
from ai_service import consultar_ia

# 1️⃣ O app TEM que ser criado ANTES de usar @app.post
app = FastAPI(
    title="Check-in Saúde API",
    description="API de análise orientativa de sintomas",
    version="1.0.0"
)

# 2️⃣ Só depois vem o endpoint
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
        print("ERRO:", e)
        raise HTTPException(
            status_code=500,
            detail="Erro ao gerar análise"
        )