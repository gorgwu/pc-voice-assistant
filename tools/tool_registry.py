import os
import importlib

from tools.base_tool import (
    BaseTool
)


class ToolRegistry:

    def __init__(self):

        self.tools = {}

        self.load_tools()

    def load_tools(self):

        tools_dir = "tools"

        for file in os.listdir(
            tools_dir
        ):

            if (
                not file.endswith(".py")
                or file.startswith("__")
                or file in [
                    "base_tool.py",
                    "tool_registry.py"
                ]
            ):
                continue

            module_name = (
                f"tools.{file[:-3]}"
            )

            module = (
                importlib.import_module(
                    module_name
                )
            )

            for attribute_name in dir(
                module
            ):

                attribute = getattr(
                    module,
                    attribute_name
                )

                if (
                    isinstance(
                        attribute,
                        type
                    )
                    and issubclass(
                        attribute,
                        BaseTool
                    )
                    and attribute != BaseTool
                ):

                    tool = (
                        attribute()
                    )

                    self.tools[
                        tool.name
                    ] = tool

    def get_tool_descriptions(
        self,
        allowed_tools: list[str]
    ):

        descriptions = []

        for tool_name in allowed_tools:

            if tool_name not in self.tools:
                continue

            tool = (
                self.tools[
                    tool_name
                ]
            )

            descriptions.append(
                f"{tool.name}: "
                f"{tool.description}"
            )

        return "\n".join(
            descriptions
        )

    def run_tool(
        self,
        tool_name: str,
        arguments: dict
    ):

        if tool_name not in self.tools:

            raise Exception(
                f"Unknown tool: "
                f"{tool_name}"
            )

        return (
            self.tools[
                tool_name
            ].run(
                arguments
            )
        )