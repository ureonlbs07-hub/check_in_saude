import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# ===============================
# SETUP BÁSICO
# ===============================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ===============================
# CARREGAMENTO DO PROMPT MASTER
# ===============================

def carregar_prompt_master() -> str:
    """
    Lê o prompt_master.py como TEXTO.
    O arquivo deve conter apenas TEXTO,
    não código Python executável.
    """
    caminho = os.path.join(os.path.dirname(__file__), "prompt_master.py")

    with open(caminho, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


# ===============================
# FUNÇÃO PRINCIPAL DE IA
# ===============================

def consultar_ia(relato_usuario: str) -> dict:
    """
    Envia o relato do usuário para a IA e exige
    EXCLUSIVAMENTE um JSON válido como resposta.
    """

    prompt_base = carregar_prompt_master()

    prompt_final = f"""
{prompt_base}

RELATO DO USUÁRIO:
{relato_usuario}

Responda OBRIGATORIAMENTE no formato JSON definido acima.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um assistente de orientação em saúde NÃO MÉDICA. "
                        "Responda SOMENTE com um JSON válido. "
                        "Não inclua explicações, comentários, markdown ou texto fora do JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt_final
                }
            ],
            temperature=0.2,
            max_tokens=600
        )

        texto = response.choices[0].message.content.strip()
        return json.loads(texto)

    except json.JSONDecodeError:
        print("⚠️ ERRO: JSON inválido retornado pela IA")
        print("📥 RESPOSTA BRUTA:")
        print(texto)

    except Exception as e:
        print("🔥 ERRO NA CONSULTA DA IA:", str(e))

    # ===============================
    # FALLBACK SEGURO (NUNCA QUEBRA O APP)
    # ===============================
    return {
        "analise_geral": "Não foi possível gerar uma análise estruturada no momento.",
        "possiveis_causas": [],
        "cuidados_gerais": [
            "Observe a evolução dos sintomas",
            "Mantenha hidratação e descanso"
        ],
        "sinais_de_alerta": [
            "Persistência ou piora dos sintomas"
        ],
        "aviso_legal": (
            "Este conteúdo é apenas informativo e não substitui "
            "avaliação ou orientação de um profissional de saúde."
        )
    }