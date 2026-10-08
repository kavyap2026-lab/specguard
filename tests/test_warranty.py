import pytest

from app.rules import check_warranty


@pytest.mark.requirement("REQ-005")
def test_warranty_before_expiry():
    covered, message = check_warranty(364)

    assert covered is True


@pytest.mark.requirement("REQ-005")
def test_warranty_at_expiry_boundary():
    covered, message = check_warranty(365)

    assert covered is True


@pytest.mark.requirement("REQ-005")
def test_warranty_after_expiry():
    covered, message = check_warranty(366)

    assert covered is False


@pytest.mark.requirement("REQ-004")
def test_warranty_future_purchase_date():
    covered, message = check_warranty(-1)

    assert covered is False
    assert message == "Purchase date cannot be in the future"