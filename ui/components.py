import streamlit as st


def render_sidebar(username):

    with st.sidebar:

        # =========================================
        # LOGO
        # =========================================

        # st.image(
        #     "public/rag-ai.png"
        # )

        st.markdown("""
        <h2 class="logo-title">
            ✨ RAG LEY AI
        </h2>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <p class="welcome-text">
            Bienvenida, {username}
        </p>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # =========================================
        # MENU
        # =========================================

        menu_items = [
            ("chat", "-", "Chat"),
            ("fuentes", "-", "Fuentes"),
            ("contratos", "-", "Contratos"),
            ("admin", "-", "Admin"),
            ("settings", "-", "Configuración")
        ]

        for page, icon, label in menu_items:

            active = st.session_state.current_page == page

            if active:

                st.markdown(f"""
                <div class="menu-active">
                    <span>{icon}</span>
                    <span>{label}</span>
                </div>
                """, unsafe_allow_html=True)

            else:

                if st.button(
                    f"{icon}  {label}",
                    key=f"menu_{page}",
                    use_container_width=True
                ):

                    st.session_state.current_page = page
                    st.rerun()

        st.markdown("---")

        # =====================================================
        # VERSION
        # =====================================================
        st.markdown("""
        <p style="
            color: #4B5563;
            font-size: 12px;
            text-align: center;
            margin-top: 20px;
        ">
            v0.1.0
        </p>
        """, unsafe_allow_html=True)