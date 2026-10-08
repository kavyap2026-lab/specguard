from specguard.html_report import generate_html_report


def test_generates_html_report(tmp_path):

    requirements = [
        {
            "id": "REQ-001",
            "title": "Return period",
            "priority": "high"
        }
    ]

    requirement_map = {
        "REQ-001": ["test_return_period"]
    }

    changes = {
        "added": [],
        "removed": [],
        "modified": []
    }

    reviewed_requirements = set()

    output_file = tmp_path / "report.html"

    generate_html_report(
        requirements=requirements,
        requirement_map=requirement_map,
        changes=changes,
        reviewed_requirements=reviewed_requirements,
        output_file=output_file
    )

    assert output_file.exists()

    content = output_file.read_text(
        encoding="utf-8"
    )

    assert "SpecGuard" in content
    assert "REQ-001" in content
    assert "100.0%" in content
    assert "test_return_period" in content