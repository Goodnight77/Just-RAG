import time
import streamlit as st

from config import Config
from models import get_embeddings, get_llm, process_pdfs, build_chain
from ui import (
    apply_custom_css,
    render_header,
    render_hero_card,
    ensure_session_state,
    render_sidebar_sessions,
)
import warnings

warnings.filterwarnings("ignore", message=".*torch.classes.*")


def main():
    """Main application function."""
    st.set_page_config(page_title=Config.PAGE_TITLE, page_icon=Config.PAGE_ICON)

    apply_custom_css()

    render_header()
    render_hero_card()

    # Ensure session state exists
    ensure_session_state()
    session_name = st.session_state.active_session
    session_data = st.session_state.sessions[session_name]

    # Render sidebar sessions
    session_name, session_data = render_sidebar_sessions(session_name, session_data)

    st.sidebar.header("Settings")
    collection_name = st.sidebar.text_input(
        "🔧 Collection Name", value=Config.DEFAULT_COLLECTION_NAME
    )
    files = st.sidebar.file_uploader(
        "📄 Upload PDFs", type="pdf", accept_multiple_files=True
    )

    # Process button
    if st.sidebar.button("Process"):
        if files:
            print(f"\n[DEBUG] Starting PDF processing for session: {session_name}")
            vs = process_pdfs(files, get_embeddings(), collection_name)
            session_data["chain"] = build_chain(vs, get_llm())
            session_data["chat_history"].clear()
            print("[DEBUG] Chain built and chat history cleared")
            st.success(
                f"✅ Processed {len(files)} file(s) into collection '{collection_name}' for {session_name}"
            )
        else:
            st.error("Upload at least one PDF!")

    # chat history
    for msg in session_data["chat_history"]:
        st.chat_message(msg["role"]).write(msg["content"])

    # Chat input
    chat_disabled = session_data["chain"] is None
    q = st.chat_input(
        "Ask about your documents..."
        if not chat_disabled
        else "Process PDFs to start chatting.",
        disabled=chat_disabled,
    )

    #user question
    if q and session_data["chain"] is not None:
        print(f"\n[DEBUG] User question: {q}")
        session_data["chat_history"].append({"role": "user", "content": q})
        with st.spinner("Thinking..."):
            t0 = time.time()
            print("[DEBUG] Querying chain...")
            ans = session_data["chain"]({"question": q})["answer"]
            response_time = time.time() - t0
            print(f"[DEBUG] Response generated in {response_time:.2f}s")
            print(
                f"[DEBUG] Answer: {ans[:100]}..."
                if len(ans) > 100
                else f"[DEBUG] Answer: {ans}"
            )
            session_data["chat_history"].append(
                {
                    "role": "assistant",
                    "content": f"{ans}\n\n⚡ Response time: {response_time:.2f}s",
                }
            )
        st.rerun()
    elif q and session_data["chain"] is None:
        st.warning("Process a document set for this session before chatting.")


if __name__ == "__main__":
    main()
