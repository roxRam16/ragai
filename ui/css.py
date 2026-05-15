import streamlit as st


def load_css():

    st.markdown("""
    <style>

    /* =======================================================
       GOOGLE FONT
    ======================================================= */

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* =======================================================
       APP
    ======================================================= */

    .stApp {
        background-color: #0E1117;
        color: white;
    }

    /* =======================================================
       SIDEBAR
    ======================================================= */

    section[data-testid="stSidebar"] {

        background-color: #111827;
        border-right: 1px solid #1F2937;
        padding-top: 10px;
    }

    /* =======================================================
       LOGO
    ======================================================= */

    .logo-title {

        color: white;
        font-size: 24px;
        font-weight: 700;

        margin-top: -5px;
        margin-bottom: 0px;

        text-align: left;
    }

    .welcome-text {

        color: #9CA3AF;
        font-size: 14px;

        text-align: left;
        margin-bottom: 20px;
    }

    /* =======================================================
       BUTTONS
    ======================================================= */

    section[data-testid="stSidebar"] .stButton button {

        background: transparent;
        border: none;

        text-align: left;

        color: #E5E7EB;

        padding: 12px 14px;

        border-radius: 10px;

        transition: all 0.2s ease;

        font-size: 15px;
        font-weight: 500;

        display: flex;
        justify-content: flex-start;

    }

    section[data-testid="stSidebar"] .stButton button:hover {

        background-color: #1F2937;
        color: white;
    }
                
    section[data-testid="stSidebar"] .stButton button div{          
        align-content:left !important;
        justify-content:left !important;
    }
                
    # .st-emotion-cache-1lads1q{
    #             # 
    # }

    /* =======================================================
       ACTIVE MENU
    ======================================================= */

    .menu-active {

        background-color: #1E293B;

        padding: 12px 14px;

        border-radius: 10px;

        color: white;

        font-weight: 600;

        display: flex;
        gap: 10px;
 

        margin-bottom: 8px;
    }

    /* =======================================================
       INPUTS
    ======================================================= */

    .stTextInput input {

        background-color: #1F2937;
        color: white;

        border: 1px solid #374151;
        border-radius: 10px;
    }

    .stTextArea textarea {

        background-color: #1F2937;
        color: white;

        border-radius: 10px;
    }

    /* =======================================================
       CHAT
    ======================================================= */

    .stChatMessage {

        background-color: #111827;
        border-radius: 14px;
        padding: 12px;
    }

    /* =======================================================
       SCROLLBAR
    ======================================================= */

    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #0E1117;
    }

    ::-webkit-scrollbar-thumb {
        background: #374151;
        border-radius: 20px;
    }

    </style>
    """, unsafe_allow_html=True)