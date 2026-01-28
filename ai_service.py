import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT_MASTER = """
Você é um assistente de orientação em saúde NÃO MÉDICA.
[... seu prompt aqui ...]
"""

def consultar_ia(relato_usuario: str) -> dict:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": PROMPT_MASTER},
                {"role": "user", "content": relato_usuario}
            ],
            temperature=0.2
        )

        texto = response.choices[0].message.content.strip()
        return json.loads(texto)

    except Exception as e:
        return {
            "analise_geral": "Erro ao gerar resposta.",
            "possiveis_causas": [],
            "cuidados_gerais": [],
            "sinais_de_alerta": [],
            "aviso_legal": "Conteúdo informativo."
        }