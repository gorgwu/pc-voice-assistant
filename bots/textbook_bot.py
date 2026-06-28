from bots.base_bot import (
    BaseBot
)


class TextbookBot(BaseBot):

    SYSTEM_PROMPT = """
    You are a helpful textbook assistant.

    Use the provided textbook (or other attached pdfs) context to answer the user's question.

    If the answer is not in the context, say that it is not in the given pdf.

    Keep responses concise and accurate.
    """

    def __init__(self):

        super().__init__(
            name="textbookbot",
            system_prompt=(
                self.SYSTEM_PROMPT
            )
        )