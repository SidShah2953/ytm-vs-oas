def discount_cashflows(cashflows, rates):
    """
    Computes the present value of cash flows discounted by given interest rates.
    
    Args:
        cashflows (list): List of future cash flows.
        rates (list or float): Discount rates for each cash flow.
    
    Returns:
        float: The present value of the cash flows.
    """
    if isinstance(rates, (int, float)):
        rates = [rates] * len(cashflows)
    
    return sum(
        cf / (1 + rate) ** (i + 1)
        for i, (cf, rate) in enumerate(zip(cashflows, rates))
    )


def calculate_bond_price(coupon_rate, ytm, face_value, years, frequency=2):
    """
    Calculates the price of a bond given its YTM.
    """
    periods = years * frequency  # Total number of coupon payments
    coupon_payment = (coupon_rate * face_value) / frequency  # Coupon per period
    periodic_ytm = ytm / frequency  # Periodic yield

    # Compute present value of each coupon using summation
    coupon_pv = sum(coupon_payment / (1 + periodic_ytm) ** t for t in range(1, periods + 1))

    # Compute present value of the face value (principal)
    principal_pv = face_value / (1 + periodic_ytm) ** periods

    # Total bond price
    price = coupon_pv + principal_pv
    
    return price
