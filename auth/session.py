<<<<<<< HEAD
# auth/session.py
import streamlit as st

def guardar_sesion(username):
    st.session_state.authenticated = True
    st.session_state.username = username


def obtener_sesion():
    return st.session_state.get("username", None)


def cerrar_sesion():
    st.session_state.authenticated = False
    st.session_state.username = None
=======
import extra_streamlit_components as stx
import streamlit as st


cookie_manager = stx.CookieManager()


def guardar_sesion(username):

    cookie_manager.set(
        "rag_user",
        username,
        expires_at=None
    )


def obtener_sesion():

    return cookie_manager.get("rag_user")


def cerrar_sesion():

    cookie_manager.delete("rag_user")
>>>>>>> 37e0176e092015d291100bcb4f3e2bef0d87ffe7
