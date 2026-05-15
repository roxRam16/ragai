import streamlit as st

from database.mongodb import get_database

from auth.login import (
    registrar_usuario,
    login_usuario
)

from ui.css import load_css
from ui.components import render_sidebar

from views.upload import render_upload_page
from views.chat import render_chat_page
from views.admin import render_admin_page
from views.settings import render_settings_page

from views.upload_fuentes import (
    render_upload_fuentes_page
)

from views.upload_contratos import (
    render_upload_contratos_page
)

from auth.session import (
    guardar_sesion,
    obtener_sesion,
    cerrar_sesion
)

db = get_database()

username = st.text_input(
    "Usuario",
    key="login_user"
)

password = st.text_input(
    "Contraseña",
    type="password",
    key="login_pass"
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button(
    "Ingresar",
    use_container_width=True
):

    ok, response = login_usuario(
        db,
        username,
        password
    )

    if ok:

        st.session_state.authenticated = True
        st.session_state.username = username
        guardar_sesion(username)

        st.rerun()

    else:
        st.error(response)
