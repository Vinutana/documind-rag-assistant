from langchain_community.vectorstores import FAISS

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)

from config import (
    GOOGLE_API_KEY,
    GEMINI_MODEL,
    EMBEDDING_MODEL,
    TOP_K
)

from prompts import RAG_PROMPT


class RAGPipeline:

    def __init__(self):

        # Initialize Gemini embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL,
            google_api_key=GOOGLE_API_KEY
        )

        # Initialize Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0.2
        )

        # Vector store
        self.vector_store = None

    # ----------------------------------------------
    # CREATE VECTOR STORE
    # ----------------------------------------------

    def create_vector_store(self, chunks):

        if not chunks:
            raise ValueError("No document chunks available.")

        self.vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=self.embeddings
        )

        return self.vector_store

    # ----------------------------------------------
    # RETRIEVE DOCUMENTS
    # ----------------------------------------------

    def retrieve_documents(self, question):

        if self.vector_store is None:
            raise ValueError(
                "Please upload and process documents first."
            )

        retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": TOP_K}
        )

        retrieved_docs = retriever.invoke(question)

        return retrieved_docs

    # ----------------------------------------------
    # FORMAT GEMINI RESPONSE
    # ----------------------------------------------

    def format_response(self, response):

        content = response.content

        # Plain text response
        if isinstance(content, str):
            return content.strip()

        # Structured Gemini content blocks
        if isinstance(content, list):

            text_parts = []

            for block in content:

                if isinstance(block, dict):

                    if block.get("type") == "text":

                        text = block.get("text", "")

                        if text:
                            text_parts.append(text)

                elif isinstance(block, str):

                    text_parts.append(block)

                elif getattr(block, "type", None) == "text":

                    text = getattr(block, "text", "")

                    if text:
                        text_parts.append(text)

            return "\n".join(text_parts).strip()

        return str(content).strip()

    # ----------------------------------------------
    # GENERATE ANSWER
    # ----------------------------------------------

    def generate_answer(
        self,
        question,
        retrieved_docs,
        chat_history=None
    ):

        # Prepare document context
        context_parts = []

        for index, doc in enumerate(
            retrieved_docs,
            start=1
        ):

            source = doc.metadata.get(
                "source", "Unknown document"
            )

            page = doc.metadata.get(
                "page", "Unknown"
            )

            context_parts.append(
                f"""
Document Context {index}

Source: {source}

Page: {page}

Content:

{doc.page_content}
"""
            )

        context = "\n\n".join(context_parts)

        # Prepare conversation history
        history_text = ""

        if chat_history:

            history_messages = []

            for message in chat_history[-6:]:

                role = message.get("role", "user")

                content = message.get("content", "")

                history_messages.append(
                    f"{role}: {content}"
                )

            history_text = "\n".join(history_messages)

        # Generate response
        chain = RAG_PROMPT | self.llm

        response = chain.invoke({
            "question": question,
            "context": context,
            "history": history_text
        })

        answer = self.format_response(response)

        return answer

    # ----------------------------------------------
    # ASK QUESTION
    # ----------------------------------------------

    def ask_question(
        self,
        question,
        chat_history=None
    ):

        if not question or not question.strip():

            raise ValueError(
                "Please enter a question."
            )

        # Retrieve relevant document chunks
        retrieved_docs = self.retrieve_documents(
            question
        )

        # Generate answer
        answer = self.generate_answer(
            question=question,
            retrieved_docs=retrieved_docs,
            chat_history=chat_history
        )

        return {
            "answer": answer,
            "sources": retrieved_docs
        }