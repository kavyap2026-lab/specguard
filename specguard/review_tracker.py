import yaml


def load_reviewed_requirements(file_path):
    """
    Load requirement IDs that have been reviewed
    after a requirement change.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    return set(data.get("reviewed_requirements", []))