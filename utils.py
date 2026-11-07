import streamlit as st


# -----------------------------------------------
# 1. Validate uploaded PDF files
# -----------------------------------------------

def validate_pdf_files(uploaded_files):

    if not uploaded_files:
        return False, "Please upload at least one PDF file."

    for file in uploaded_files:

        if not file.name.lower().endswith(".pdf"):
            return False, f"{file.name} is not a PDF file."

        if file.size == 0:
            return False, f"{file.name} is empty."

        # Maximum file size: 20 MB per PDF
        if file.size > 20 * 1024 * 1024:
            return False, f"{file.name} exceeds the 20 MB limit."

    return True, "Files validated successfully."


# -----------------------------------------------
# 2. Format document source references
# -----------------------------------------------

def format_sources(source_documents):

    sources = []
    seen_sources = set()

    for document in source_documents:

        source_name = document.metadata.get(
            "source", "Unknown document"
        )

        page_number = document.metadata.get(
            "page", "Unknown"
        )

        source_key = (source_name, page_number)

        if source_key not in seen_sources:

            sources.append({
                "document": source_name,
                "page": page_number
            })

            seen_sources.add(source_key)

    return sources


# -----------------------------------------------
# 3. Display source references in Streamlit
# -----------------------------------------------

def display_sources(source_documents):

    sources = format_sources(source_documents)

    if not sources:
        return

    with st.expander("View sources"):

        for source in sources:

            st.markdown(
                f"- **{source['document']}** "
                f"— Page {source['page']}"
            )


# -----------------------------------------------
# 4. Display application errors
# -----------------------------------------------

def display_error(error_message):

    st.error(error_message)


# -----------------------------------------------
# 5. Display application success messages
# -----------------------------------------------

def display_success(success_message):

    st.success(success_message)