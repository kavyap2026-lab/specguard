from specguard.change_detector import detect_requirement_changes


def test_detects_modified_requirement():

    old_requirements = [
        {
            "id": "REQ-001",
            "title": "Premium return period",
            "description": "Return within 30 days"
        }
    ]

    new_requirements = [
        {
            "id": "REQ-001",
            "title": "Premium return period",
            "description": "Return within 45 days"
        }
    ]

    changes = detect_requirement_changes(
        old_requirements,
        new_requirements
    )

    assert len(changes["modified"]) == 1
    assert changes["modified"][0]["id"] == "REQ-001"

def test_detects_added_requirement():

    old_requirements = []

    new_requirements = [
        {
            "id": "REQ-008",
            "title": "Refund processing",
            "description": "Refund must be processed"
        }
    ]

    changes = detect_requirement_changes(
        old_requirements,
        new_requirements
    )

    assert len(changes["added"]) == 1
    assert changes["added"][0]["id"] == "REQ-008"


def test_detects_removed_requirement():

    old_requirements = [
        {
            "id": "REQ-009",
            "title": "Legacy return rule",
            "description": "Old return rule"
        }
    ]

    new_requirements = []

    changes = detect_requirement_changes(
        old_requirements,
        new_requirements
    )

    assert len(changes["removed"]) == 1
    assert changes["removed"][0]["id"] == "REQ-009"


def test_no_changes_when_requirements_are_identical():

    requirements = [
        {
            "id": "REQ-001",
            "title": "Return period",
            "description": "Return within 14 days"
        }
    ]

    changes = detect_requirement_changes(
        requirements,
        requirements
    )

    assert len(changes["added"]) == 0
    assert len(changes["removed"]) == 0
    assert len(changes["modified"]) == 0