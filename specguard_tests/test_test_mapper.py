from specguard.test_mapper import find_requirement_tests


def test_maps_requirement_to_test(tmp_path):

    test_file = tmp_path / "test_example.py"

    test_file.write_text(
        """
import pytest


@pytest.mark.requirement("REQ-001")
def test_standard_return():
    assert True


@pytest.mark.requirement("REQ-002")
def test_premium_return():
    assert True
""",
        encoding="utf-8"
    )

    mapping = find_requirement_tests(tmp_path)

    assert "REQ-001" in mapping
    assert "REQ-002" in mapping

    assert mapping["REQ-001"] == [
        "test_standard_return"
    ]

    assert mapping["REQ-002"] == [
        "test_premium_return"
    ]

def test_maps_multiple_tests_to_same_requirement(tmp_path):

    test_file = tmp_path / "test_boundaries.py"

    test_file.write_text(
        """
import pytest


@pytest.mark.requirement("REQ-001")
def test_before_boundary():
    assert True


@pytest.mark.requirement("REQ-001")
def test_at_boundary():
    assert True


@pytest.mark.requirement("REQ-001")
def test_after_boundary():
    assert True
""",
        encoding="utf-8"
    )

    mapping = find_requirement_tests(tmp_path)

    assert len(mapping["REQ-001"]) == 3

    assert mapping["REQ-001"] == [
        "test_before_boundary",
        "test_at_boundary",
        "test_after_boundary"
    ]

def test_ignores_tests_without_requirement_marker(tmp_path):

    test_file = tmp_path / "test_example.py"

    test_file.write_text(
        """
import pytest


@pytest.mark.requirement("REQ-001")
def test_mapped():
    assert True


def test_without_requirement():
    assert True
""",
        encoding="utf-8"
    )

    mapping = find_requirement_tests(tmp_path)

    assert mapping["REQ-001"] == [
        "test_mapped"
    ]

    assert "test_without_requirement" not in mapping["REQ-001"]