import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT_MASTER = """
Você é um assistente de orientação em saúde NÃO MÉDICA.

REGRAS:
- Não prescreva medicamentos.
- Não sugira terapias alternativas, naturais ou complementares.
- Não faça diagnósticos.
- Seja conciso, claro e humano.

FORMATO OBRIGATÓRIO (JSON):
{
  "analise_geral": "",
  "possiveis_causas": [],
  "cuidados_gerais": [],
  "sinais_de_alerta": [],
  "aviso_legal": ""
}
"""

def consultar_ia(relato_usuario: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": PROMPT_MASTER},
                {"role": "user", "content": f"RELATO DO USUÁRIO:\n{relato_usuario}"}
            ],
            temperature=0.2,
            max_tokens=500
        )

        return json.loads(response.choices[0].message.content.strip())

    except Exception as e:
        print("ERRO IA:", e)
        return {
            "analise_geral": "Não foi possível gerar análise no momento.",
            "possiveis_causas": [],
            "cuidados_gerais": ["Observe a evolução dos sintomas"],
            "sinais_de_alerta": ["Persistência ou piora dos sintomas"],
            "aviso_legal": "Conteúdo informativo. Não substitui avaliação profissional."
        }