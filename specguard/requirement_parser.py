import yaml


def load_requirements(file_path):
    """
    Load requirements from a YAML file.

    Args:
        file_path: Path to the requirements YAML file.

    Returns:
        list: List of requirement dictionaries.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return data.get("requirements", [])