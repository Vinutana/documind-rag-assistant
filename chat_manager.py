from datetime import datetime
from uuid import uuid4


class ChatManager:
    """
    Manages chat sessions, messages, and uploaded document names.
    Chat data is maintained in Streamlit session state.
    """

    def __init__(self, session_state):
        self.session_state = session_state
        self.initialize()

    # -----------------------------------------------
    # 1. Initialize chat storage
    # -----------------------------------------------

    def initialize(self):

        if "chats" not in self.session_state:
            self.session_state["chats"] = {}

        if "active_chat_id" not in self.session_state:
            self.session_state["active_chat_id"] = None

    # -----------------------------------------------
    # 2. Create a new chat
    # -----------------------------------------------

    def create_chat(self):

        chat_id = str(uuid4())
        current_time = datetime.now().astimezone().isoformat()

        self.session_state["chats"][chat_id] = {
            "id": chat_id,
            "title": "New Chat",
            "created_at": current_time,
            "updated_at": current_time,
            "messages": [],
            "documents": []
        }

        self.session_state["active_chat_id"] = chat_id

        return chat_id

    # -----------------------------------------------
    # 3. Get active chat
    # -----------------------------------------------

    def get_active_chat(self):

        chat_id = self.session_state.get("active_chat_id")

        if not chat_id:
            return None

        return self.session_state["chats"].get(chat_id)

    # -----------------------------------------------
    # 4. Switch between chats
    # -----------------------------------------------

    def switch_chat(self, chat_id):

        if chat_id not in self.session_state["chats"]:
            raise ValueError("Chat session not found.")

        self.session_state["active_chat_id"] = chat_id

        return self.get_active_chat()

    # -----------------------------------------------
    # 5. Add a message to the active chat
    # -----------------------------------------------

    def add_message(self, role, content):

        if role not in ["user", "assistant"]:
            raise ValueError("Role must be user or assistant.")

        chat = self.get_active_chat()

        if chat is None:
            self.create_chat()
            chat = self.get_active_chat()

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().astimezone().isoformat()
        }

        chat["messages"].append(message)

        chat["updated_at"] = datetime.now().astimezone().isoformat()

        # Generate title from the first user question
        if role == "user" and chat["title"] == "New Chat":

            title = content.strip().replace("\n", " ")

            if len(title) > 40:
                title = title[:37] + "..."

            chat["title"] = title or "New Chat"

        return message

    # -----------------------------------------------
    # 6. Get conversation history
    # -----------------------------------------------

    def get_chat_history(self, chat_id=None):

        if chat_id is None:
            chat = self.get_active_chat()
        else:
            chat = self.session_state["chats"].get(chat_id)

        if chat is None:
            return []

        return chat["messages"]

    # -----------------------------------------------
    # 7. Get history for RAG pipeline
    # -----------------------------------------------

    def get_rag_history(self):

        messages = self.get_chat_history()

        # Exclude timestamps; RAG pipeline needs role/content
        return [
            {
                "role": message["role"],
                "content": message["content"]
            }
            for message in messages
        ]

    # -----------------------------------------------
    # 8. Add uploaded document names
    # -----------------------------------------------

    def add_documents(self, document_names):

        chat = self.get_active_chat()

        if chat is None:
            self.create_chat()
            chat = self.get_active_chat()

        for document_name in document_names:

            if document_name not in chat["documents"]:
                chat["documents"].append(document_name)

        chat["updated_at"] = datetime.now().astimezone().isoformat()

    # -----------------------------------------------
    # 9. Get uploaded documents
    # -----------------------------------------------

    def get_documents(self):

        chat = self.get_active_chat()

        if chat is None:
            return []

        return chat["documents"]

    # -----------------------------------------------
    # 10. Get all chat sessions
    # -----------------------------------------------

    def get_all_chats(self):

        chats = self.session_state["chats"].values()

        return sorted(
            chats,
            key=lambda chat: chat["updated_at"],
            reverse=True
        )

    # -----------------------------------------------
    # 11. Delete a chat
    # -----------------------------------------------

    def delete_chat(self, chat_id):

        if chat_id not in self.session_state["chats"]:
            return

        del self.session_state["chats"][chat_id]

        if self.session_state["active_chat_id"] == chat_id:

            remaining_chats = self.get_all_chats()

            if remaining_chats:
                self.session_state["active_chat_id"] = (
                    remaining_chats[0]["id"]
                )
            else:
                self.session_state["active_chat_id"] = None