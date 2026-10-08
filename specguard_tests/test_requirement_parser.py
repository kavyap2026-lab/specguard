from specguard.requirement_parser import load_requirements


def test_loads_requirements_from_yaml(tmp_path):

    yaml_file = tmp_path / "requirements.yaml"

    yaml_file.write_text(
        """
requirements:
  - id: REQ-001
    title: Return period
    description: Products may be returned within 14 days.
    category: returns
    priority: high

  - id: REQ-002
    title: Warranty period
    description: Products have a 365 day warranty.
    category: warranty
    priority: high
""",
        encoding="utf-8"
    )

    requirements = load_requirements(yaml_file)

    assert len(requirements) == 2

    assert requirements[0]["id"] == "REQ-001"
    assert requirements[0]["title"] == "Return period"

    assert requirements[1]["id"] == "REQ-002"
    assert requirements[1]["title"] == "Warranty period"

def test_returns_empty_list_when_no_requirements_exist(tmp_path):

    yaml_file = tmp_path / "requirements.yaml"

    yaml_file.write_text(
        """
version: "1.0"
requirements: []
""",
        encoding="utf-8"
    )

    requirements = load_requirements(yaml_file)

    assert requirements == []