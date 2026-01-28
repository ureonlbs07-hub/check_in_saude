import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT_MASTER = """
(seu prompt aqui)
"""

def consultar_ia(relato_usuario: str):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": PROMPT_MASTER},
            {"role": "user", "content": relato_usuario}
        ],
        temperature=0.2,
        max_tokens=500
    )

    return json.loads(response.choices[0].message.content)