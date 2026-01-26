import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def consultar_ia(prompt: str) -> dict:
    """
    Envia um prompt para a IA e espera EXCLUSIVAMENTE um JSON válido como resposta.
    Retorna um dicionário Python.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Você deve responder EXCLUSIVAMENTE com um JSON válido. "
                    "Não inclua comentários, explicações, markdown ou texto fora do JSON."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=700
    )

    texto = response.choices[0].message.content.strip()

    try:
        return json.loads(texto)

    except json.JSONDecodeError as e:
        # DEBUG CONTROLADO (essencial em MVP)
        print("⚠️ ERRO: IA retornou JSON inválido")
        print("📥 RESPOSTA BRUTA:")
        print(texto)
        print("📛 ERRO JSON:", str(e))

        # Retorno seguro para não quebrar o app
        return {
            "analise_geral": "Não foi possível gerar uma resposta estruturada no momento.",
            "possiveis_causas": [],
            "cuidados_gerais": [],
            "sinais_de_alerta": [
                "Se o desconforto persistir, procure um profissional de saúde."
            ],
            "aviso_legal": (
                "Este conteúdo é apenas informativo e educativo e "
                "não substitui avaliação ou orientação profissional."
            )
        }