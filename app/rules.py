def check_return_eligibility(customer_type, days_since_purchase, quantity, damaged=False):
    """
    Determine whether a product is eligible for return.

    Returns:
        tuple: (eligible, message)
    """

    if quantity < 1:
        return False, "Return quantity must be at least 1"

    if days_since_purchase < 0:
        return False, "Purchase date cannot be in the future"

    if damaged:
        return False, "Damaged products require a warranty claim"

    if customer_type == "standard":
        if days_since_purchase <= 14:
            return True, "Return approved"
        return False, "Standard return period expired"

    if customer_type == "premium":
        if days_since_purchase <= 45:
            return True, "Return approved"
        return False, "Premium return period expired"

    return False, "Invalid customer type"
def check_warranty(days_since_purchase):
    """
    Determine whether a product is covered by warranty.
    """

    if days_since_purchase < 0:
        return False, "Purchase date cannot be in the future"

    if days_since_purchase <= 365:
        return True, "Product is under warranty"

    return False, "Warranty expired"