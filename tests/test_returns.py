import pytest

from app.rules import check_return_eligibility


@pytest.mark.requirement("REQ-001")
def test_standard_return_before_boundary():
    eligible, message = check_return_eligibility(
        customer_type="standard",
        days_since_purchase=13,
        quantity=1
    )

    assert eligible is True


@pytest.mark.requirement("REQ-001")
def test_standard_return_at_boundary():
    eligible, message = check_return_eligibility(
        customer_type="standard",
        days_since_purchase=14,
        quantity=1
    )

    assert eligible is True


@pytest.mark.requirement("REQ-001")
def test_standard_return_after_boundary():
    eligible, message = check_return_eligibility(
        customer_type="standard",
        days_since_purchase=15,
        quantity=1
    )

    assert eligible is False

@pytest.mark.requirement("REQ-002")
def test_premium_return_before_boundary():
    eligible, message = check_return_eligibility(
        customer_type="premium",
        days_since_purchase=44,
        quantity=1
    )

    assert eligible is True


@pytest.mark.requirement("REQ-002")
def test_premium_return_at_boundary():
    eligible, message = check_return_eligibility(
        customer_type="premium",
        days_since_purchase=45,
        quantity=1
    )

    assert eligible is True


@pytest.mark.requirement("REQ-002")
def test_premium_return_after_boundary():
    eligible, message = check_return_eligibility(
        customer_type="premium",
        days_since_purchase=46,
        quantity=1
    )

    assert eligible is False

@pytest.mark.requirement("REQ-003")
def test_return_quantity_zero():
    eligible, message = check_return_eligibility(
        customer_type="standard",
        days_since_purchase=5,
        quantity=0
    )

    assert eligible is False
    assert message == "Return quantity must be at least 1"


@pytest.mark.requirement("REQ-003")
def test_return_quantity_one():
    eligible, message = check_return_eligibility(
        customer_type="standard",
        days_since_purchase=5,
        quantity=1
    )

    assert eligible is True


@pytest.mark.requirement("REQ-003")
def test_return_quantity_negative():
    eligible, message = check_return_eligibility(
        customer_type="standard",
        days_since_purchase=5,
        quantity=-1
    )

    assert eligible is False
    assert message == "Return quantity must be at least 1"

@pytest.mark.requirement("REQ-004")
def test_future_purchase_date():
    eligible, message = check_return_eligibility(
        customer_type="standard",
        days_since_purchase=-1,
        quantity=1
    )

    assert eligible is False
    assert message == "Purchase date cannot be in the future"


@pytest.mark.requirement("REQ-004")
def test_purchase_today():
    eligible, message = check_return_eligibility(
        customer_type="standard",
        days_since_purchase=0,
        quantity=1
    )

    assert eligible is True

@pytest.mark.requirement("REQ-006")
def test_damaged_product_normal_return():
    eligible, message = check_return_eligibility(
        customer_type="standard",
        days_since_purchase=5,
        quantity=1,
        damaged=True
    )

    assert eligible is False
    assert message == "Damaged products require a warranty claim"


@pytest.mark.requirement("REQ-006")
def test_non_damaged_product_normal_return():
    eligible, message = check_return_eligibility(
        customer_type="standard",
        days_since_purchase=5,
        quantity=1,
        damaged=False
    )

    assert eligible is True

@pytest.mark.requirement("REQ-007")
def test_invalid_customer_type():
    eligible, message = check_return_eligibility(
        customer_type="gold",
        days_since_purchase=5,
        quantity=1
    )

    assert eligible is False
    assert message == "Invalid customer type"