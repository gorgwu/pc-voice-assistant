from bots.base_bot import (
    BaseBot
)


class InterviewBot(BaseBot):

    SYSTEM_PROMPT = """
    You are a professional technical interviewer.
    
    Your responsibilities:
    - ask concise follow-up questions
    - probe implementation details
    - challenge vague answers
    - remain conversational
    
    Keep responses under 3 sentences.
    """

    def __init__(self):

        super().__init__(
            name="interviewbot",
            system_prompt=(
                self.SYSTEM_PROMPT
            )
        )