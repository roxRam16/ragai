import streamlit as st


def render_upload_contratos_page():

    st.title("📄 Contratos")

    st.markdown("""
    Sube:

    - contratos
    - anexos
    - convenios
    - expedientes
    """)

    uploaded = st.file_uploader(
        "Sube contratos",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded:
        st.success(f"{len(uploaded)} contratos listos")