import streamlit as st

from auth.session import guardar_sesion

from auth.security import verify_password


def render_login(db):

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("""
        <div class="login-box">

        <h1 style='text-align:center;'>
        ✨ RAG LEY AI
        </h1>

        <p style='text-align:center; opacity:0.7;'>
        Plataforma Inteligente
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        username = st.text_input(
            "Usuario"
        )

        password = st.text_input(
            "Contraseña",
            type="password"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "Ingresar",
            use_container_width=True
        ):

            usuario = db["usuarios"].find_one({
                "username": username
            })

            if not usuario:
                st.error("Usuario no encontrado")
                return

            if not verify_password(
                password,
                usuario["password"]
            ):
                st.error("Contraseña incorrecta")
                return

            guardar_sesion(username)

            st.session_state.authenticated = True
            st.session_state.username = username

            st.rerun()