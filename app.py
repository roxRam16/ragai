import streamlit as st
import asyncio
import sys

from database.mongodb import get_database

from ui.css import load_css
from ui.components import render_sidebar

from auth.session import (
    guardar_sesion,
    obtener_sesion,
    cerrar_sesion
)

from auth.login import render_login

from views.chat import render_chat_page
from views.admin import render_admin_page
from views.settings import render_settings_page
from views.upload_fuentes import render_upload_fuentes_page
from views.upload_contratos import render_upload_contratos_page



# Silenciar el error de asyncio en Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="RAG LEY AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS
# =========================================================

load_css()

# =========================================================
# SESSION STATE
# =========================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "chat"

# =========================================================
# DATABASE
# =========================================================

db = get_database()

# =========================================================
# RESTORE SESSION
# =========================================================

saved_user = obtener_sesion()

if saved_user:

    st.session_state.authenticated = True
    st.session_state.username = saved_user

# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.authenticated:

    render_login(db)

    st.stop()

# =========================================================
# SIDEBAR
# =========================================================

render_sidebar(
    st.session_state.username
)

st.sidebar.markdown("---")

# =========================================================
# MENU
# =========================================================

# if st.sidebar.button(
#     "💬 Chat",
#     use_container_width=True,
#     key="chat_btn"
# ):
#     st.session_state.current_page = "chat"

# if st.sidebar.button(
#     "📚 Fuentes",
#     use_container_width=True,
#     key="fuentes_btn"
# ):
#     st.session_state.current_page = "fuentes"

# if st.sidebar.button(
#     "📄 Contratos",
#     use_container_width=True,
#     key="contratos_btn"
# ):
#     st.session_state.current_page = "contratos"

# if st.sidebar.button(
#     "📊 Admin",
#     use_container_width=True,
#     key="admin_btn"
# ):
#     st.session_state.current_page = "admin"

# if st.sidebar.button(
#     "⚙️ Configuración",
#     use_container_width=True,
#     key="settings_btn"
# ):
#     st.session_state.current_page = "settings"

# st.sidebar.markdown("---")

# =========================================================
# LOGOUT
# =========================================================

if st.sidebar.button(
    "🚪 Cerrar sesión",
    use_container_width=True,
    key="logout_btn"
):

    cerrar_sesion()

    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.current_page = "chat"

    st.rerun()

# =========================================================
# MAIN CONTENT
# =========================================================

page = st.session_state.current_page

if page == "chat":
    render_chat_page()

elif page == "fuentes":
    render_upload_fuentes_page()

elif page == "contratos":
    render_upload_contratos_page()

elif page == "admin":
    render_admin_page()

elif page == "settings":
    render_settings_page()