import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT_MASTER = """
Você é um assistente de orientação em saúde NÃO MÉDICA.

Regras obrigatórias:
- Não faça diagnósticos.
- Não prescreva medicamentos.
- Não use termos médicos conclusivos.
- Use linguagem clara, humana e probabilística.

Objetivo:
Analisar o relato do usuário e gerar uma resposta PERSONALIZADA,
mostrando claramente que o texto foi compreendido.

Formato da resposta:
1. Análise orientativa baseada no relato
2. Possíveis causas comuns (hipotéticas)
3. Cuidados gerais
4. Sinais de alerta

Nunca responda de forma genérica.
Sempre cite elementos do relato do usuário.
"""

def consultar_ia(relato_usuario: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": PROMPT_MASTER},
                {
                    "role": "user",
                    "content": f'Relato do usuário:\n"""{relato_usuario}"""'
                }
            ],
            max_tokens=500,
            temperature=0.3
        )

        return response.choices[0].message["content"].strip()

    except Exception as e:
        print("ERRO OPENAI REAL:", repr(e))
        return (
            "No momento não consegui processar sua mensagem. "
            "Se os sintomas persistirem ou piorarem, procure um serviço de saúde."
        )