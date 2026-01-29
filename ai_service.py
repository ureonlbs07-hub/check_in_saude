import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT_MASTER = """
Você é um assistente de orientação em saúde não médica.
Não faça diagnósticos.
Não prescreva medicamentos.
Use linguagem educativa, humana e probabilística.
"""

def consultar_ia(relato_usuario: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": PROMPT_MASTER},
                {"role": "user", "content": relato_usuario}
            ],
            max_tokens=300,
            temperature=0.2
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print("ERRO OPENAI REAL:", repr(e))
        return (
            "No momento não consegui processar sua mensagem. "
            "Se os sintomas persistirem ou piorarem, procure um serviço de saúde."
        )