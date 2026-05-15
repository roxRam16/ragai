import os
import hashlib
import tempfile
import streamlit as st
import time

from rag.chunking import crear_chunks
from rag.pdf_processing import procesar_pdf

from database.mongodb import (
    get_database,
    guardar_chunks,
    obtener_documentos
)

def render_upload_fuentes_page():

    st.markdown("""
    <h1 style='font-size:32px;'>
    📚 Base de conocimiento
    </h1>
    """, unsafe_allow_html=True)

    st.caption(
        "Sube leyes, reglamentos, contratos o lineamientos para alimentar el RAG."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # KEY DINÁMICA para resetear uploader
    # =====================================================
    if "upload_key" not in st.session_state:
        st.session_state.upload_key = 0

    uploaded_file = st.file_uploader(
        "Selecciona un PDF",
        type=["pdf"],
        label_visibility="collapsed",
        key=f"uploader_{st.session_state.upload_key}"
    )

    col1, col2 = st.columns([1, 5])

    with col1:
        procesar = st.button(
            "Subir",
            use_container_width=True,
            type="primary"
        )

    # =====================================================
    # PROCESS
    # =====================================================

    if procesar:

        if not uploaded_file:
            st.warning("Selecciona un archivo PDF")
            return

        db = get_database()

        # =====================================================
        # VERIFICAR DUPLICADO POR HASH
        # =====================================================
        contenido = uploaded_file.read()
        hash_archivo = hashlib.md5(contenido).hexdigest()

        existe = db["documentos"].find_one({
            "metadata.hash": hash_archivo
        })

        if existe:
            st.warning(
                f"⚠️ **{uploaded_file.name}** ya existe en la base de conocimiento."
            )
            return

        progress = st.progress(0)
        status = st.empty()

        try:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as tmp:
                tmp.write(contenido)  # ya lo leímos arriba
                tmp_path = tmp.name

            status.info("📄 Extrayendo texto...")
            progress.progress(20)
            texto, fue_ocr = procesar_pdf(tmp_path)

            status.info("✂️ Creando chunks...")
            progress.progress(45)
            chunks = crear_chunks(
                texto,
                chunk_size=1000,
                chunk_overlap=200
            )

            metadata = {
                "nombre_archivo": uploaded_file.name,
                "hash": hash_archivo,
                "tipo": "fuente",
                "fue_ocr": fue_ocr
            }

            status.info("🧠 Generando embeddings...")
            progress.progress(70)

            total_guardados = guardar_chunks(chunks, metadata)

            progress.progress(100)

            # =====================================================
            # TOAST + RESET
            # =====================================================
            status.empty()
            progress.empty()

            st.toast(
                f"✅ {uploaded_file.name} — {total_guardados} chunks guardados",
                icon="🎉"
            )

            time.sleep(2.5)          # 👈 agregar aquí

            #st.cache_data.clear() 

            st.session_state.upload_key += 1

            st.rerun()

        except Exception as e:
            st.error(str(e))

        finally:
            if "tmp_path" in locals() and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # ARCHIVOS CARGADOS
    # =====================================================

    st.markdown("## 📁 Archivos cargados")

    documentos = obtener_documentos()

    if not documentos:
        st.info("Aún no hay documentos cargados.")

    else:

        archivos_unicos = {}

        for doc in documentos:
            metadata = doc.get("metadata", {})
            nombre = metadata.get("nombre_archivo", "Sin nombre")
            fue_ocr = metadata.get("fue_ocr", False)

            if nombre not in archivos_unicos:
                archivos_unicos[nombre] = {
                    "fue_ocr": fue_ocr,
                    "chunks": 1
                }
            else:
                archivos_unicos[nombre]["chunks"] += 1

        for nombre, info in archivos_unicos.items():

            ocr_badge = "🔍 OCR" if info["fue_ocr"] else "📝 Nativo"

            st.markdown(f"""
            <div style="
                background:#161B22;
                padding:14px 18px;
                border-radius:12px;
                margin-bottom:10px;
                border:1px solid #30363D;
                display:flex;
                justify-content:space-between;
                align-items:center;
            ">
                <span>📄 <b>{nombre}</b></span>
                <span style="color:#9CA3AF; font-size:13px;">
                    {ocr_badge} &nbsp;·&nbsp; {info["chunks"]} chunks
                </span>
            </div>
            """, unsafe_allow_html=True)