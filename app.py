import ast
import streamlit as st

from config import APP_NAME, APP_DESCRIPTION

from chat_manager import ChatManager
from rag_pipeline import RAGPipeline
from document_processor import process_uploaded_pdfs

from utils import validate_pdf_files


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title=APP_NAME,
    page_icon="📚",
    layout="wide"
)

st.title("📚DocuMind")
st.caption(APP_DESCRIPTION)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

chat_manager = ChatManager(st.session_state)

if "rag_pipelines" not in st.session_state:
    st.session_state["rag_pipelines"] = {}


def get_pipeline(chat_id):

    pipelines = st.session_state["rag_pipelines"]

    if chat_id not in pipelines:
        pipelines[chat_id] = RAGPipeline()

    return pipelines[chat_id]


# --------------------------------------------------
# CLEAN ANSWER
# --------------------------------------------------

def clean_answer(answer):

    if isinstance(answer, str):

        try:

            parsed = ast.literal_eval(answer)

            if isinstance(parsed, list):

                text_parts = []

                for block in parsed:

                    if isinstance(block, dict):

                        text = block.get("text", "")

                        if text:
                            text_parts.append(text)

                if text_parts:
                    return "\n".join(text_parts).strip()

        except (ValueError, SyntaxError):
            pass

        return answer.strip()

    if isinstance(answer, list):

        text_parts = []

        for block in answer:

            if isinstance(block, dict):

                text = block.get("text", "")

                if text:
                    text_parts.append(text)

            elif isinstance(block, str):

                text_parts.append(block)

        return "\n".join(text_parts).strip()

    if isinstance(answer, dict):

        return answer.get("text", str(answer)).strip()

    return str(answer).strip()


# --------------------------------------------------
# SOURCE DISPLAY
# --------------------------------------------------

def show_sources(sources):

    if not sources:
        return

    with st.expander("View Sources"):

        seen = set()

        for source in sources:

            document = source.metadata.get(
                "source", "Unknown document"
            )

            page = source.metadata.get(
                "page", "Unknown"
            )

            source_key = (document, page)

            if source_key not in seen:

                st.markdown(
                    f"- **{document}** — Page {page}"
                )

                seen.add(source_key)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title(" 📚DocuMind")

    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):

        chat_manager.create_chat()
        st.rerun()

    st.divider()

    st.subheader("Chat History")

    for chat in chat_manager.get_all_chats():

        if st.button(
            chat["title"],
            key=f"chat_{chat['id']}",
            use_container_width=True
        ):

            chat_manager.switch_chat(chat["id"])
            st.rerun()

    st.divider()

    active_chat = chat_manager.get_active_chat()

    if active_chat is None:

        chat_manager.create_chat()

    active_chat = chat_manager.get_active_chat()

    chat_id = active_chat["id"]

    # PDF upload
    st.subheader("Upload Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button(
        "Process Documents",
        use_container_width=True
    ):

        is_valid, message = validate_pdf_files(
            uploaded_files
        )

        if not is_valid:

            st.error(message)

        else:

            try:

                with st.spinner(
                    "Processing your documents..."
                ):

                    chunks = process_uploaded_pdfs(
                        uploaded_files
                    )

                    pipeline = get_pipeline(chat_id)

                    pipeline.create_vector_store(chunks)

                    document_names = [
                        file.name for file in uploaded_files
                    ]

                    chat_manager.add_documents(
                        document_names
                    )

                st.success(
                    "Documents processed successfully!"
                )

            except Exception as error:

                st.error(
                    f"Document processing failed: {error}"
                )

    st.divider()

    st.subheader("Uploaded Documents")

    documents = chat_manager.get_documents()

    if documents:

        for document in documents:

            st.write(f"📄 {document}")

    else:

        st.caption("No documents uploaded yet.")


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

active_chat = chat_manager.get_active_chat()

if active_chat:

    for message in chat_manager.get_chat_history():

        with st.chat_message(message["role"]):

            if message["role"] == "assistant":

                answer = clean_answer(
                    message["content"]
                )

                st.markdown(answer)

                show_sources(
                    message.get("sources", [])
                )

            else:

                st.markdown(
                    message["content"]
                )


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

question = st.chat_input(
    "Ask a question about your documents..."
)

if question:

    active_chat = chat_manager.get_active_chat()

    chat_id = active_chat["id"]

    pipeline = get_pipeline(chat_id)

    if pipeline.vector_store is None:

        st.warning(
            "Please upload and process your PDF documents first."
        )

    else:

        # Get previous conversation history
        chat_history = chat_manager.get_rag_history()

        # Save user message
        chat_manager.add_message(
            "user",
            question
        )

        with st.chat_message("user"):

            st.markdown(question)

        with st.chat_message("assistant"):

            try:

                with st.spinner(
                    "Generating answer..."
                ):

                    result = pipeline.ask_question(
                        question=question,
                        chat_history=chat_history
                    )

                    answer = clean_answer(
                        result["answer"]
                    )

                # Display formatted answer
                st.markdown(answer)

                # Display source references
                sources = result.get("sources", [])

                show_sources(sources)

                # Save assistant answer
                assistant_message = chat_manager.add_message(
                    "assistant",
                    answer
                )

                assistant_message["sources"] = sources

            except Exception as error:

                st.error(
                    f"Unable to generate answer: {error}"
                )

                st.exception(error)