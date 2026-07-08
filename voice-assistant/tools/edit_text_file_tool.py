import os

from google import genai

from config import (
    GEMINI_API_KEY,
    MODEL_NAME
)

from tools.base_tool import (
    BaseTool
)


class EditTextFileTool(
    BaseTool
):

    name = (
        "edit_text_file"
    )

    description = """
    Edits an existing text file.

    Arguments:
    - filename
    - instruction
    """

    WORKSPACE = "workspace"

    def __init__(self):

        self.client = (
            genai.Client(
                api_key=GEMINI_API_KEY
            )
        )

    def run(
        self,
        arguments: dict
    ):

        filename = arguments[
            "filename"
        ]

        instruction = arguments[
            "instruction"
        ]

        file_path = os.path.join(
            self.WORKSPACE,
            filename
        )

        if not os.path.exists(
            file_path
        ):

            return (
                "File does not exist."
            )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            current_text = (
                f.read()
            )

        prompt = f"""
You are editing a text file.

Current file:

{current_text}

Instruction:

{instruction}

Return ONLY the updated file contents.
Do not explain changes.
"""

        response = (
            self.client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
        )

        updated_text = (
            response.text
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                updated_text
            )

        return (
            f"Updated file: "
            f"{filename}"
        )