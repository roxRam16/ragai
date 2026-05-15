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


new_user = st.text_input(
    "Nuevo usuario",
    key="register_user"
)

new_pass = st.text_input(
    "Nueva contraseña",
    type="password",
    key="register_pass"
)

confirm_pass = st.text_input(
    "Confirmar contraseña",
    type="password",
    key="register_confirm"
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button(
    "Crear cuenta",
    use_container_width=True
):
    if not new_user:
        st.error("Ingresa un usuario")

    elif not new_pass:
        st.error("Ingresa una contraseña")

    elif new_pass != confirm_pass:
        st.error("Las contraseñas no coinciden")

    else:

        ok, msg = registrar_usuario(
            db,
            new_user,
            new_pass
        )

        if ok:
            st.success(msg)

        else:
            st.error(msg)