from ai.memory import (
    ConversationMemory
)


class BaseBot:

    capability_tags = ()
    tool_names = ()

    def __init__(
        self,
        name: str,
        system_prompt: str,
        tools: list[str] = None
    ):

        self.name = name

        self.system_prompt = (
            system_prompt
        )

        self.capabilities = (
            set(self.capability_tags)
        )

        self.tools = (
            list(tools)
            if tools is not None
            else list(self.tool_names)
        )

        self.memory = (
            ConversationMemory()
        )

    def has_capability(
        self,
        tag: str
    ) -> bool:

        return tag in self.capabilities

    def build_prompt(
        self,
        user_message: str,
        context: str = "",
        tool_descriptions: str = ""
    ):

        history = (
            self.memory.build_history()
        )

        tool_section = ""

        if tool_descriptions:

            tool_section = f"""
Available Tools:

{tool_descriptions}
"""

        prompt = f"""
{self.system_prompt}

{tool_section}

Conversation History:

{history}

Context:

{context}

User:

{user_message}

Assistant:
"""

        return prompt

    def save_interaction(
        self,
        user_message: str,
        assistant_message: str
    ):

        self.memory.add_user_message(
            user_message
        )

        self.memory.add_assistant_message(
            assistant_message
        )