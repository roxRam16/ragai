import os

from dotenv import load_dotenv

from openai import OpenAI

# cargar .env
load_dotenv()


def generar_embedding(texto):

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texto
    )

    return response.data[0].embedding