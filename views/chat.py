import os
import streamlit as st
from openai import OpenAI

from rag.retrieval import buscar_chunks_similares
from rag.prompts import PROMPT_RAG
from database.mongodb import get_database


def render_chat_page():

    st.title("💬 RAG LEY AI")

    db = get_database()
    collection = db["documentos"]

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # =====================================================
    # HISTORIAL
    # =====================================================
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # =====================================================
    # INPUT
    # =====================================================
    prompt = st.chat_input("Pregunta algo sobre la ley...")

    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )

            # =============================================
            # DETECTAR PREGUNTA GENERAL
            # =============================================
            preguntas_generales = [
                "qué eres", "quién eres", "con qué ley",
                "para qué sirves", "qué puedes hacer",
                "cómo funciona", "qué documentos",
                "con que ley", "que ley"
            ]

            es_general = any(
                p in prompt.lower()
                for p in preguntas_generales
            )

            with st.spinner("Buscando en documentos..."):

                if es_general:
                    chunks = []
                else:
                    chunks = buscar_chunks_similares(
                        pregunta=prompt,
                        collection=collection,
                        top_k=5
                    )

            # =============================================
            # RESPUESTA SIN CONTEXTO (pregunta general)
            # =============================================
            if not chunks:

                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    stream=True,
                    messages=[
                        {
                            "role": "system",
                            "content": PROMPT_RAG
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                respuesta = st.write_stream(stream)

            # =============================================
            # RESPUESTA CON CONTEXTO (pregunta sobre ley)
            # =============================================
            else:

                contexto = "\n\n---\n\n".join([
                    c.get("texto", "") for c in chunks
                ])

                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    stream=True,
                    messages=[
                        {
                            "role": "system",
                            "content": PROMPT_RAG
                        },
                        {
                            "role": "user",
                            "content": f"""
CONTEXTO:
{contexto}

PREGUNTA:
{prompt}
"""
                        }
                    ]
                )

                respuesta = st.write_stream(stream)

        st.session_state.messages.append({
            "role": "assistant",
            "content": respuesta
        })