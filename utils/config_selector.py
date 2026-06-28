import os
import inquirer


def select_config(config_dir="configs"):

    if not os.path.exists(config_dir):
        raise Exception("configs/ folder not found")

    files = [
        f for f in os.listdir(config_dir)
        if f.endswith(".json")
    ]

    if not files:
        raise Exception("No config files found in configs/")

    choices = [
        f"{config_dir}/{f}" for f in files
    ]

    questions = [
        inquirer.List(
            "config",
            message="Select a config file",
            choices=choices,
        )
    ]

    answer = inquirer.prompt(questions)

    return answer["config"]