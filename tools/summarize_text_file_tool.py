import os

from tools.base_tool import (
    BaseTool
)


class SummarizeTextFileTool(
    BaseTool
):

    name = (
        "summarize_text_file"
    )

    description = """
    Reads a text file and
    returns its contents.

    Arguments:
    - filename
    """

    WORKSPACE = "workspace"

    def run(
        self,
        arguments: dict
    ):

        filename = arguments[
            "filename"
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

            text = f.read()

        return text