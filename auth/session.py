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