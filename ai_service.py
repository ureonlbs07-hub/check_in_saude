import os
from dotenv import load_dotenv
from openai import OpenAI

# Carrega variáveis de ambiente (.env local / Render em produção)
load_dotenv()

# Cliente OpenAI (SDK novo)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Prompt mestre (não médico, variável, conciso)
PROMPT_MASTER = """
Você é um assistente de orientação em saúde não médica.

Analise cada relato como um caso único.
Adapte o tom e o nível de detalhe conforme a situação descrita.
Seja claro, humano e direto, sem respostas padronizadas.

Não faça diagnósticos.
Não prescreva medicamentos.
Não se apresente como médico.
Use linguagem probabilística e educativa.
"""

def consultar_ia(relato_usuario: str) -> str:
    """
    Envia o relato do usuário para a OpenAI e retorna
    uma resposta textual segura e orientativa.
    """
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": PROMPT_MASTER
                },
                {
                    "role": "user",
                    "content": relato_usuario
                }
            ],
            max_output_tokens=300,
            temperature=0.2
        )

        # 🔎 EXTRAÇÃO ROBUSTA DO TEXTO (forma correta da Responses API)
        if hasattr(response, "output") and response.output:
            for item in response.output:
                if item.get("type") == "message":
                    for content in item.get("content", []):
                        if content.get("type") == "output_text":
                            texto = content.get("text", "").strip()
                            if texto:
                                return texto

        # Se a IA respondeu, mas não retornou texto utilizável
        return (
            "Não foi possível gerar uma resposta clara neste momento. "
            "Se os sintomas persistirem ou piorarem, procure um serviço de saúde."
        )

    except Exception as e:
        # Log completo no terminal do Render
        print("ERRO NA IA (OpenAI):", repr(e))

        # Resposta segura para o app
        return (
            "No momento não consegui processar sua mensagem. "
            "Se os sintomas persistirem ou piorarem, procure um serviço de saúde."
        )