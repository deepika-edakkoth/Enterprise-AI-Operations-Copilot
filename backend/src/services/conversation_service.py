import uuid

class ConversationService:

    @staticmethod
    def create_conversation():
        return str(uuid.uuid4())