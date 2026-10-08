from specguard.review_tracker import load_reviewed_requirements


def test_loads_reviewed_requirements(tmp_path):

    review_file = tmp_path / "review_status.yaml"

    review_file.write_text(
        """
reviewed_requirements:
  - REQ-002
  - REQ-005
""",
        encoding="utf-8"
    )

    reviewed = load_reviewed_requirements(review_file)

    assert "REQ-002" in reviewed
    assert "REQ-005" in reviewed
    assert len(reviewed) == 2


def test_returns_empty_set_when_no_reviews_exist(tmp_path):

    review_file = tmp_path / "review_status.yaml"

    review_file.write_text(
        """
reviewed_requirements: []
""",
        encoding="utf-8"
    )

    reviewed = load_reviewed_requirements(review_file)

    assert reviewed == set()