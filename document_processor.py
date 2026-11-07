import pymupdf
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_SIZE, CHUNK_OVERLAP


def extract_text_from_pdf(uploaded_file):
    """
    Extract text from a PDF while preserving page metadata.
    """

    documents = []

    pdf_bytes = uploaded_file.getvalue()

    pdf = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    for page_number, page in enumerate(pdf, start=1):

        text = page.get_text("text").strip()

        if not text:
            continue

        document = Document(
            page_content=text,
            metadata={
                "source": uploaded_file.name,
                "page": page_number
            }
        )

        documents.append(document)

    pdf.close()

    return documents


def split_documents(documents):
    """
    Split extracted documents into smaller chunks.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


def process_uploaded_pdfs(uploaded_files):
    """
    Process multiple uploaded PDF files.
    """

    all_documents = []

    for uploaded_file in uploaded_files:

        documents = extract_text_from_pdf(uploaded_file)

        all_documents.extend(documents)

    if not all_documents:
        raise ValueError(
            "No readable text was found in the uploaded PDFs."
        )

    chunks = split_documents(all_documents)

    if not chunks:
        raise ValueError(
            "Unable to generate document chunks."
        )

    return chunks