import os
from dotenv import load_dotenv
from openai import OpenAI

# Carrega variáveis do .env
load_dotenv()

# Inicializa cliente OpenAI usando a variável de ambiente
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

PROMPT_MASTER = """
Você é um assistente educacional de saúde não médica.

Analise cada relato como um caso único.
Adapte o tom, o foco e a profundidade da resposta conforme:
– a gravidade aparente
– a clareza do relato
– o tipo de sintoma descrito

Evite respostas padronizadas ou fórmulas repetidas.
Não use listas fixas nem estruturas obrigatórias.
Escreva de forma natural, como um profissional experiente explicando algo
de maneira clara e responsável.

Use linguagem probabilística.
Não faça diagnósticos.
Não prescreva medicamentos nem indique doses.
Se mencionar tratamentos ou medicamentos, faça apenas de forma informativa
e contextual, sem recomendação direta.

Priorize respostas concisas, úteis e acolhedoras.
Inclua alertas para procurar atendimento apenas quando fizer sentido
diante do relato apresentado.

Nunca afirme certezas clínicas.
Nunca se apresente como médico.
Deixe implícito que a resposta é orientativa e educacional.
"""

def consultar_ia(relato_usuario: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": PROMPT_MASTER},
                {"role": "user", "content": relato_usuario}
            ],
            temperature=0.2,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        # Loga o erro no terminal (para debug)
        print("ERRO NA IA:", e)

        # Resposta segura para o app (nunca quebra)
        return (
            "No momento não consegui processar sua mensagem. "
            "Se os sintomas persistirem ou piorarem, procure um serviço de saúde."
        )