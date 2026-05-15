import streamlit as st


def render_chat_page():

    st.title("💬 RAG LEY AI")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # HISTORIAL

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            st.markdown(msg["content"])

    # INPUT

    prompt = st.chat_input(
        "Pregunta algo..."
    )

    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        # IA RESPONSE

        response = f"""
        Respuesta simulada para:

        {prompt}
        """

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })