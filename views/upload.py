import streamlit as st
import tempfile
import os

from rag.chunking import crear_chunks
from rag.embeddings import generar_embedding



def render_upload_page():

    st.title("📄 Cargar documentos")

    uploaded_file = st.file_uploader(
        "Sube un PDF",
        type=['pdf']
    )

    if uploaded_file:

        st.success(
            f"Archivo cargado: {uploaded_file.name}"
        )