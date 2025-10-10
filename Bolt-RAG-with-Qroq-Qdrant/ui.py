"""UI components and styling for Bolt RAG Streamlit application."""

import streamlit as st
from models import get_logo_data_uri


def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app."""
    st.markdown(
        """
        <style>
            .stApp {
                background: radial-gradient(circle at top, #1b1f3a 0%, #080b16 55%, #05060d 100%);
                color: #f8fafc;
            }
            .main > div {
                padding-top: 1.2rem;
            }
            div[data-testid="stSidebar"] {
                background: linear-gradient(180deg, rgba(12, 18, 35, 0.95) 0%, rgba(7, 9, 20, 0.95) 100%);
                border-right: 1px solid rgba(148, 163, 184, 0.15);
            }
            .hero-card {
                background: rgba(15, 23, 42, 0.55);
                border: 1px solid rgba(59, 130, 246, 0.15);
                box-shadow: 0 18px 45px rgba(14, 35, 94, 0.45);
                border-radius: 18px;
                padding: 1.4rem 1.6rem;
                backdrop-filter: blur(9px);
                margin-bottom: 1.4rem;
            }
            .hero-card h3 {
                margin: 0 0 0.6rem 0;
                font-size: 1.3rem;
                color: #f8fafc;
            }
            .hero-card p {
                margin: 0;
                color: #cbd5f5;
                line-height: 1.55;
            }
            .badge-row {
                display: flex;
                flex-wrap: wrap;
                gap: 0.6rem;
                margin-top: 0.9rem;
            }
            .badge {
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
                padding: 0.35rem 0.75rem;
                border-radius: 999px;
                border: 1px solid rgba(148, 163, 184, 0.25);
                background: rgba(30, 64, 175, 0.25);
                font-size: 0.75rem;
                letter-spacing: 0.01em;
                color: #e0e7ff;
            }
            .stButton > button {
                background: linear-gradient(135deg, #f97316 0%, #ec4899 100%);
                color: #fff;
                border-radius: 999px;
                border: none;
                padding: 0.5rem 1.1rem;
                font-weight: 600;
                box-shadow: 0 12px 30px rgba(236, 72, 153, 0.35);
            }
            .stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 14px 36px rgba(236, 72, 153, 0.45);
            }
            [data-testid="stSidebar"] .stButton > button {
                width: 100%;
                box-shadow: none;
            }
            [data-testid="stSidebar"] .stButton > button:hover {
                box-shadow: none;
            }
            [data-testid="stSidebar"] .stTextInput input {
                border-radius: 12px;
                border: 1px solid rgba(148, 163, 184, 0.4);
            }
            [data-testid="stFileUploader"] details {
                border-radius: 12px;
                border: 1px dashed rgba(96, 165, 250, 0.45);
                background: rgba(12, 74, 110, 0.1);
            }
            [data-testid="stChatMessage"] {
                border-radius: 18px;
                border: 1px solid rgba(148, 163, 184, 0.2);
                background: rgba(15, 23, 42, 0.45);
                padding: 1rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    """Render the application header with logo."""
    logo_src = get_logo_data_uri()
    logo_img_html = (
        f'<img src="{logo_src}" alt="Qdrant" width="32" style="margin-left: 6px;">'
        if logo_src
        else ""
    )
    st.markdown(
        f"""
    <div style="text-align: center;">
        <h2 style="display: inline-flex; align-items: center; justify-content: center; color: white; gap: 6px;">
            Bolt RAG using
            <span style="color: #ff6f00;">Groq</span> & 
            <a href="https://qdrant.tech" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; text-decoration: none; color: inherit;">
                <span style="color: #DC244C;">Qdrant</span>
                {logo_img_html}
            </a>
        </h2>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_hero_card():
    """Render the hero card with app description and features."""
    st.markdown(
        """
        <div class="hero-card">
            <h3>Chat faster, learn deeper ⚡</h3>
            <p>Upload your PDFs, let Cohere embeddings index the knowledge, then query with Groq-powered reasoning backed by Qdrant recall. Bolt RAG keeps it speedy without sacrificing context.</p>
            <div class="badge-row">
                <span class="badge">🚀 Groq instant inference</span>
                <span class="badge">🧠 Cohere embeddings</span>
                <span class="badge">🗂️ Conversational memory</span>
                <span class="badge">🔍 Top-4 dense retrieval</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def create_new_session(set_active=True):
    """Create a new chat session bucket in Streamlit session state."""
    if "sessions" not in st.session_state:
        st.session_state.sessions = {}
        st.session_state.active_session = None

    idx = len(st.session_state.sessions) + 1
    name = f"Session {idx}"
    while name in st.session_state.sessions:
        idx += 1
        name = f"Session {idx}"

    st.session_state.sessions[name] = {"chain": None, "chat_history": []}
    if set_active or st.session_state.active_session is None:
        st.session_state.active_session = name
    return name


def ensure_session_state():
    """Ensure at least one chat session exists for the UI."""
    if "sessions" not in st.session_state or not st.session_state.sessions:
        create_new_session(set_active=True)


def render_sidebar_sessions(session_name, session_data):
    """
    Render session management in sidebar.

    Args:
        session_name: Current active session name
        session_data: Current session data

    Returns:
        tuple: (updated_session_name, updated_session_data)
    """
    st.sidebar.subheader("💬 Sessions")
    if st.sidebar.button("➕ New Chat Session"):
        create_new_session()
        st.rerun()

    session_labels = list(st.session_state.sessions.keys())
    if session_name not in session_labels:
        session_name = session_labels[0]
        st.session_state.active_session = session_name
        session_data = st.session_state.sessions[session_name]

    selected_session = st.sidebar.selectbox(
        "Active Session",
        session_labels,
        index=session_labels.index(session_name),
    )
    if selected_session != session_name:
        st.session_state.active_session = selected_session
        session_name = selected_session
        session_data = st.session_state.sessions[session_name]

    if session_data["chat_history"]:
        st.sidebar.markdown("#### Recent Turns")
        for msg in reversed(session_data["chat_history"][-4:]):
            icon = "🧑‍💻" if msg["role"] == "user" else "🤖"
            preview = msg["content"].split("\n")[0]
            trimmed = preview[:60] + ("…" if len(preview) > 60 else "")
            st.sidebar.caption(f"{icon} {trimmed}")

    st.sidebar.markdown(
        '<hr style="border: 2px solid #ff6f00; width: 100%; margin-top: 10px; margin-bottom: 10px;">',
        unsafe_allow_html=True,
    )

    return session_name, session_data
