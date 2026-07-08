from abc import ABC
from abc import abstractmethod


class BaseTool(ABC):

    name = ""
    description = ""

    @abstractmethod
    def run(
        self,
        arguments: dict
    ):
        pass