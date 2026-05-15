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