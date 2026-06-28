import os

from tools.base_tool import (
    BaseTool
)


class CreateTextFileTool(
    BaseTool
):

    name = (
        "create_text_file"
    )

    description = """
    Creates a text file.

    Arguments:
    - filename
    - text
    """

    WORKSPACE = "workspace"

    def run(
        self,
        arguments: dict
    ):

        filename = arguments[
            "filename"
        ]

        text = arguments[
            "text"
        ]

        os.makedirs(
            self.WORKSPACE,
            exist_ok=True
        )

        file_path = os.path.join(
            self.WORKSPACE,
            filename
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(text)

        return (
            f"Created file: "
            f"{filename}"
        )