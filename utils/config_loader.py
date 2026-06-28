import json


class ConfigLoader:

    def load(
        self,
        config_path: str
    ):

        with open(
            config_path,
            "r"
        ) as f:

            config = json.load(f)

        return config