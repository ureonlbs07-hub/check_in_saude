import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT_MASTER = """
Você é um assistente de orientação em saúde NÃO MÉDICA.

REGRAS OBRIGATÓRIAS:
1. Não prescreva medicamentos.
2. Não sugira terapias alternativas, naturais, tradicionais ou complementares.
3. Não mencione medicina chinesa, homeopatia, chás, ervas ou suplementos.
4. Não faça diagnósticos.
5. Seja conciso, claro e direto.
6. Use linguagem simples e humana.
7. Nunca se coloque como médico.

REGRAS DE ESTILO:
- Máximo de 3 frases por campo textual.
- Listas com no máximo 5 itens.
- Não repita informações entre os campos.

FORMATO OBRIGATÓRIO DA RESPOSTA (JSON):
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

        texto = response.choices[0].message.content.strip()
        return json.loads(texto)

    except Exception as e:
        print("ERRO IA:", e)

        return {
            "analise_geral": "Não foi possível gerar uma análise no momento.",
            "possiveis_causas": [],
            "cuidados_gerais": [
                "Observe a evolução dos sintomas",
                "Mantenha descanso e hidratação"
            ],
            "sinais_de_alerta": [
                "Persistência ou piora dos sintomas"
            ],
            "aviso_legal": (
                "Este conteúdo é apenas informativo e não substitui avaliação profissional."
            )
        }