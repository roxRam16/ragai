import streamlit as st

from auth.security import hash_password

from datetime import datetime


def render_register(db):

    st.subheader("Crear cuenta")

    username = st.text_input(
        "Usuario",
        key="register_user"
    )

    password = st.text_input(
        "Contraseña",
        type="password",
        key="register_pass"
    )

    confirm = st.text_input(
        "Confirmar contraseña",
        type="password",
        key="register_confirm"
    )

    if st.button(
        "Crear cuenta",
        use_container_width=True
    ):

        if password != confirm:
            st.error("Las contraseñas no coinciden")
            return

        existe = db["usuarios"].find_one({
            "username": username
        })

        if existe:
            st.error("El usuario ya existe")
            return

        db["usuarios"].insert_one({
            "username": username,
            "password": hash_password(password),

            "nombre": "",
            "apellidos": "",
            "fecha_nacimiento": "",
            "telefono": "",
            "empresa": "",
            "puesto": "",

            "created_at": datetime.utcnow(),
            "activo": True
        })

        st.success("Usuario creado")