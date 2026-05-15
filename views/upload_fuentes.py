import os
import tempfile
import streamlit as st

from rag.chunking import crear_chunks
from rag.pdf_processing import procesar_pdf

from database.mongodb import (
    get_database,
    guardar_chunks,
    obtener_documentos
)

# =========================================================
# PAGE
# =========================================================

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
    # UPLOAD BOX
    # =====================================================

    uploaded_file = st.file_uploader(
        "Selecciona un PDF",
        type=["pdf"],
        label_visibility="collapsed"
    )

    col1, col2 = st.columns([1,5])

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

        progress = st.progress(0)

        status = st.empty()

        try:

            # =============================================
            # DATABASE
            # =============================================

            db = get_database()

            # =============================================
            # TEMP FILE
            # =============================================

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as tmp:

                tmp.write(uploaded_file.read())

                tmp_path = tmp.name

            # =============================================
            # OCR / PDF
            # =============================================

            status.info("📄 Extrayendo texto...")

            progress.progress(20)

            texto, fue_ocr = procesar_pdf(tmp_path)

            # =============================================
            # CHUNKS
            # =============================================

            status.info("✂️ Creando chunks...")

            progress.progress(45)

            chunks = crear_chunks(
                texto,
                chunk_size=1000,
                chunk_overlap=200
            )

            # =============================================
            # METADATA
            # =============================================

            metadata = {

                "nombre_archivo": uploaded_file.name,

                "tipo": "fuente",

                "fue_ocr": fue_ocr
            }

            # =============================================
            # SAVE VECTORIAL
            # =============================================

            status.info("🧠 Generando embeddings...")

            progress.progress(70)

            total_guardados = guardar_chunks(
                db,
                chunks,
                metadata
            )

            progress.progress(100)

            status.success("✅ Documento procesado correctamente")

            st.success(
                f"""
                Archivo: {uploaded_file.name}

                Chunks generados: {len(chunks)}

                Chunks guardados: {total_guardados}
                """
            )

            # =============================================
            # PREVIEW
            # =============================================

            with st.expander("👁️ Preview del primer chunk"):

                st.text_area(
                    "Chunk",
                    chunks[0],
                    height=250
                )

        except Exception as e:

            st.error(str(e))

        finally:

            if "tmp_path" in locals() and os.path.exists(tmp_path):

                os.unlink(tmp_path)

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # FILES LIST
    # =====================================================

    st.markdown("## 📁 Archivos cargados")

    documentos = obtener_documentos()

    if not documentos:

        st.info("Aún no hay documentos")

    else:

        archivos_unicos = set()

        for doc in documentos:

            metadata = doc.get("metadata", {})

            nombre = metadata.get(
                "nombre_archivo",
                "Sin nombre"
            )

            if nombre in archivos_unicos:
                continue

            archivos_unicos.add(nombre)

            st.markdown(f"""
            <div style="
                background:#161B22;
                padding:14px;
                border-radius:12px;
                margin-bottom:10px;
                border:1px solid #30363D;
            ">

            📄 <b>{nombre}</b>

            </div>
            """, unsafe_allow_html=True)