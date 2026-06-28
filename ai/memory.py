class ConversationMemory:

    def __init__(self):

        self.messages = []

    def add_user_message(
        self,
        message: str
    ):

        self.messages.append({
            "role": "user",
            "content": message
        })

    def add_assistant_message(
        self,
        message: str
    ):

        self.messages.append({
            "role": "assistant",
            "content": message
        })

    def build_history(self):

        history = ""

        for msg in self.messages:

            history += (
                f"{msg['role']}: "
                f"{msg['content']}\n"
            )

        return history