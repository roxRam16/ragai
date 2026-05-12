"""
Aplicación Streamlit para gestión de documentos RAG - LOPSRM
"""
import streamlit as st
import os
from dotenv import load_dotenv
import tempfile
from utils import (
    get_database,
    procesar_pdf,
    crear_chunks,
    guardar_en_mongodb
)

# Cargar variables de entorno
load_dotenv()

# Configuración de página
st.set_page_config(
    page_title="RAG LOPSRM - Gestión de Documentos",
    page_icon="📚",
    layout="wide"
)


def check_login(username: str, password: str) -> bool:
    """Verificar credenciales de login"""
    admin_user = os.getenv("ADMIN_USERNAME", "admin")
    admin_pass = os.getenv("ADMIN_PASSWORD", "lopsrm2024")
    
    return username == admin_user and password == admin_pass


def login_page():
    """Página de login"""
    st.title("🔐 Sistema RAG - LOPSRM")
    st.markdown("### Inicio de sesión")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("Iniciar sesión", use_container_width=True)
            
            if submit:
                if check_login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos")


def main_app():
    """Aplicación principal"""
    
    # Sidebar
    with st.sidebar:
        st.title("👤 Usuario")
        st.write(f"**{st.session_state.username}**")
        if st.button("Cerrar sesión", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
        
        st.divider()
        st.markdown("### 📊 Estadísticas")
        
        # Conectar a BD y obtener stats
        try:
            db = get_database()
            collection_name = os.getenv("MONGODB_COLLECTION", "documentos_legales")
            collection = db[collection_name]
            
            total_docs = collection.count_documents({})
            
            # Contar por tipo
            tipos = collection.distinct("metadata.tipo_documento")
            
            st.metric("Total de chunks", total_docs)
            
            for tipo in tipos:
                count = collection.count_documents({"metadata.tipo_documento": tipo})
                st.metric(f"Tipo: {tipo}", count)
                
        except Exception as e:
            st.error(f"Error conectando a BD: {e}")
    
    # Contenido principal
    st.title("📚 Gestión de Documentos - RAG LOPSRM")
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📤 Cargar documentos", "🔍 Buscar", "⚙️ Configuración"])
    
    with tab1:
        cargar_documentos_tab()
    
    with tab2:
        st.info("🚧 La funcionalidad de búsqueda estará disponible en la Fase 2")
        st.markdown("""
        En esta fase podrás:
        - Buscar por similitud semántica
        - Filtrar por tipo de documento
        - Ver documentos relacionados
        """)
    
    with tab3:
        configuracion_tab()


def cargar_documentos_tab():
    """Tab para cargar documentos"""
    
    st.header("Carga de documentos PDF")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Upload de archivo
        uploaded_file = st.file_uploader(
            "Selecciona un archivo PDF",
            type=['pdf'],
            help="Sube contratos, leyes o lineamientos en formato PDF"
        )
    
    with col2:
        # Tipo de documento
        tipo_documento = st.selectbox(
            "Tipo de documento",
            ["Contrato", "LOPSRM", "Lineamiento SFP", "Reglamento", "Otro"],
            help="Clasificación del documento"
        )
    
    # Metadatos adicionales
    with st.expander("📋 Metadatos adicionales (opcionales)"):
        col_meta1, col_meta2 = st.columns(2)
        
        with col_meta1:
            dependencia = st.text_input("Dependencia")
            numero_contrato = st.text_input("Número de contrato/expediente")
        
        with col_meta2:
            fecha_documento = st.date_input("Fecha del documento")
            tags = st.text_input("Tags (separados por coma)")
    
    # Opciones de procesamiento
    st.markdown("### ⚙️ Opciones de procesamiento")
    
    col_opt1, col_opt2 = st.columns(2)
    
    with col_opt1:
        chunk_size = st.slider(
            "Tamaño de chunk (caracteres)",
            min_value=500,
            max_value=2000,
            value=1000,
            step=100,
            help="Cantidad de caracteres por fragmento"
        )
    
    with col_opt2:
        chunk_overlap = st.slider(
            "Overlap entre chunks",
            min_value=0,
            max_value=500,
            value=200,
            step=50,
            help="Caracteres compartidos entre fragmentos"
        )
    
    # Botón de procesamiento
    if st.button("🚀 Procesar y subir a MongoDB", type="primary", use_container_width=True):
        if uploaded_file is None:
            st.error("⚠️ Por favor selecciona un archivo PDF")
            return
        
        # Guardar archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        
        try:
            with st.spinner("Procesando documento..."):
                # Crear contenedor de progreso
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Paso 1: Extraer texto
                status_text.text("📄 Extrayendo texto del PDF...")
                progress_bar.progress(20)
                texto, fue_ocr = procesar_pdf(tmp_path)
                
                if fue_ocr:
                    st.info("ℹ️ Se detectó un PDF escaneado. Se aplicó OCR.")
                
                # Paso 2: Crear chunks
                status_text.text("✂️ Dividiendo en fragmentos...")
                progress_bar.progress(40)
                chunks = crear_chunks(texto, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                
                st.info(f"📊 Se crearon {len(chunks)} fragmentos")
                
                # Paso 3: Preparar metadatos
                status_text.text("📝 Preparando metadatos...")
                progress_bar.progress(60)
                
                metadata = {
                    "tipo_documento": tipo_documento,
                    "nombre_archivo": uploaded_file.name,
                    "dependencia": dependencia if dependencia else "No especificada",
                    "numero_contrato": numero_contrato if numero_contrato else "N/A",
                    "fecha_documento": fecha_documento.isoformat() if fecha_documento else None,
                    "tags": [tag.strip() for tag in tags.split(",")] if tags else [],
                    "fue_ocr": fue_ocr,
                    "chunk_size": chunk_size,
                    "chunk_overlap": chunk_overlap
                }
                
                # Paso 4: Generar embeddings y guardar
                status_text.text("🧠 Generando embeddings y guardando en MongoDB...")
                progress_bar.progress(80)
                
                db = get_database()
                docs_insertados = guardar_en_mongodb(chunks, metadata, db)
                
                progress_bar.progress(100)
                status_text.text("✅ Proceso completado!")
                
                st.success(f"""
                ✅ **Documento procesado exitosamente**
                
                - **Archivo:** {uploaded_file.name}
                - **Tipo:** {tipo_documento}
                - **Chunks creados:** {len(chunks)}
                - **Documentos insertados:** {docs_insertados}
                """)
                
                # Mostrar preview del primer chunk
                with st.expander("👁️ Preview del primer fragmento"):
                    st.text_area("Texto", chunks[0], height=200)
        
        except Exception as e:
            st.error(f"❌ Error procesando el documento: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
        
        finally:
            # Limpiar archivo temporal
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


def configuracion_tab():
    """Tab de configuración"""
    st.header("Configuración del sistema")
    
    st.markdown("### 🔧 Variables de entorno")
    
    # Verificar configuración
    config_items = {
        "MongoDB URI": os.getenv("MONGODB_URI", "❌ No configurado"),
        "Base de datos": os.getenv("MONGODB_DATABASE", "lopsrm_rag"),
        "Colección": os.getenv("MONGODB_COLLECTION", "documentos_legales"),
        "Modelo de embeddings": os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        "OpenAI API Key": "✅ Configurado" if os.getenv("OPENAI_API_KEY") else "❌ No configurado"
    }
    
    for key, value in config_items.items():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"**{key}:**")
        with col2:
            if "❌" in str(value):
                st.error(value)
            else:
                st.success(value)
    
    st.markdown("---")
    st.markdown("### 📚 Crear índice vectorial en MongoDB Atlas")
    
    st.info("""
    **⚠️ IMPORTANTE:** Antes de poder hacer búsquedas, necesitas crear el índice vectorial en MongoDB Atlas.
    
    **Pasos:**
    1. Ve a tu cluster en MongoDB Atlas
    2. Entra a la pestaña "Search"
    3. Click en "Create Search Index"
    4. Selecciona "JSON Editor"
    5. Copia y pega la configuración de abajo
    """)
    
    index_config = {
        "fields": [
            {
                "type": "vector",
                "path": "embedding",
                "numDimensions": 1536,
                "similarity": "cosine"
            },
            {
                "type": "filter",
                "path": "metadata.tipo_documento"
            },
            {
                "type": "filter",
                "path": "metadata.tags"
            }
        ]
    }
    
    st.code(str(index_config).replace("'", '"'), language="json")
    
    st.markdown("""
    **Nombra tu índice como:** `vector_index`
    
    Después de crear el índice, podrás hacer búsquedas semánticas en la pestaña "Buscar".
    """)


# Control de flujo principal
def main():
    # Inicializar session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # Mostrar login o app
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()


if __name__ == "__main__":
    main()
