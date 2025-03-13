import numpy as np
from helpers.finance import calculate_bond_price
from helpers.dataCollection import get_implied_volatility

n_simulations = 100000


def determine_call_threshold(coupon_rate,
                             call_years,
                             treasury_rates,
                             call_spread=0.005):
    """
    Determines the threshold interest rate at which the issuer is likely to call the bond.
    
    Args:
        coupon_rate (float): The coupon rate of the bond.
        call_years (int): Years until the bond is callable.
        treasury_rates (dict): Treasury rates by maturity.
        call_spread (float): Spread above risk-free rate for refinancing.
    
    Returns:
        float: The call threshold interest rate.
    """
    risk_free_rate_at_call = treasury_rates[call_years]
    call_threshold = risk_free_rate_at_call + call_spread
    return min(call_threshold, coupon_rate)


# def mcs_call_probability(coupon_rate, 
#                          treasury_rates,
#                          n_simulations=n_simulations,
#                          call_years=3):
#     """
#     Simulates interest rate paths and estimates the probability of the bond being called.
    
#     Args:
#         coupon_rate (float): The coupon rate of the bond.
#         treasury_rates (dict): Treasury rates by maturity.
#         n_simulations (int): Number of simulations.
#         n_years (int): Number of years to simulate.
#         volatility (float): Interest rate volatility.
    
#     Returns:
#         float: Probability that the bond will be called.
#     """
#     volatility = get_implied_volatility()

#     call_threshold = determine_call_threshold(
#         coupon_rate=coupon_rate,
#         call_years=call_years,
#         treasury_rates=treasury_rates
#     )
    
#     call_count = 0
#     for _ in range(n_simulations):
#         # Focus on year 3 when the bond becomes callable
#         base_rate = treasury_rates[3]  # 3-year Treasury rate
#         simulated_rate = base_rate * np.exp(np.random.normal(0, volatility))
        
#         # If the simulated rate drops below the call threshold, the bond is likely to be called
#         if simulated_rate < call_threshold:
#             call_count += 1
    
#     return call_count / n_simulations


# def calculate_oas_from_ytm(face_value,
#                            coupon_rate,
#                            frequency,
#                            years,
#                            ytm,
#                            treasury_rates,
#                            call_years=3,
#                            n_simulations=n_simulations):
#     """
#     Calculates the Option-Adjusted Spread (OAS) given a fixed YTM.
    
#     Args:
#         coupon_rate (float): The bond's coupon rate.
#         ytm (float): The bond's yield to maturity.
#         face_value (float): The bond's face value.
#         treasury_rates (dict): Dictionary of Treasury rates by maturity.
#         years (int): Years to maturity.
#         call_years (int): Years until callable.
#         n_simulations (int): Number of Monte Carlo simulations.
        
#     Returns:
#         tuple: (OAS in basis points, Bond price)
#     """
#     # Calculate bond price based on YTM
#     bond_price = calculate_bond_price(coupon_rate, ytm, face_value, years)
    
#     # Estimate call probability
#     call_probability = mcs_call_probability(
#         coupon_rate=coupon_rate,
#         treasury_rates=treasury_rates,
#         n_simulations=n_simulations
#     )
    
#     # Calculate expected value of the bond based on call probability
#     call_periods = call_years * frequency
#     total_periods = years * frequency
#     coupon_payment = (coupon_rate / frequency) * face_value
    
#     # Calculate present value if called
#     pv_if_called = 0
#     for i in range(call_periods):
#         period_rate = treasury_rates[min(7, max(3, (i + 1) // frequency + 1))]
#         pv_if_called += coupon_payment / (1 + period_rate/frequency)**(i + 1)
    
#     # Add present value of principal at call date
#     pv_if_called += face_value / (1 + treasury_rates[call_years]/frequency)**call_periods
    
#     # Calculate present value if not called
#     pv_if_not_called = 0
#     for i in range(total_periods):
#         period_rate = treasury_rates[min(7, max(3, (i + 1) // frequency + 1))]
#         pv_if_not_called += coupon_payment / (1 + period_rate/frequency)**(i + 1)
    
#     # Add present value of principal at maturity
#     pv_if_not_called += face_value / (1 + treasury_rates[years]/frequency)**total_periods
    
#     # Calculate expected value
#     expected_value_no_spread = call_probability * pv_if_called + (1 - call_probability) * pv_if_not_called
    
#     # Calculate OAS as the spread needed to equate expected value to bond price
#     # This is the spread that needs to be added to Treasury rates to make the expected value equal to the bond price
#     oas = (ytm - treasury_rates[years]) - (expected_value_no_spread - bond_price) / bond_price
    
#     return oas * 10000  # Convert to basis points

import scipy.optimize as opt

def mcs_call_probability(coupon_rate, treasury_rates, ytm, n_simulations=n_simulations, call_years=3):
    """
    Simulates interest rate paths and estimates the probability of the bond being called dynamically for each YTM.
    """
    volatility = get_implied_volatility()
    call_threshold = determine_call_threshold(
        coupon_rate=coupon_rate,
        call_years=call_years,
        treasury_rates=treasury_rates
    )
    
    call_count = 0
    for _ in range(n_simulations):
        base_rate = treasury_rates[3]
        simulated_rate = base_rate * np.exp(np.random.normal(0, volatility))
        if simulated_rate < call_threshold:
            call_count += 1
    
    return call_count / n_simulations


def calculate_oas_from_ytm(face_value, coupon_rate, frequency, years, ytm, treasury_rates, call_years=3, n_simulations=n_simulations):
    """
    Calculates the Option-Adjusted Spread (OAS) given a fixed YTM using numerical root-finding.
    """
    bond_price = calculate_bond_price(coupon_rate, ytm, face_value, years)
    call_probability = mcs_call_probability(
        coupon_rate=coupon_rate,
        treasury_rates=treasury_rates,
        ytm=ytm,
        n_simulations=n_simulations
    )
    
    def bond_price_with_spread(spread):
        """Computes the expected present value of bond cash flows given a spread."""
        call_periods = call_years * frequency
        total_periods = years * frequency
        coupon_payment = (coupon_rate / frequency) * face_value
        
        pv_if_called = sum(
            coupon_payment / (1 + treasury_rates[min(7, max(3, (i + 1) // frequency + 1))] + spread / frequency) ** (i + 1)
            for i in range(call_periods)
        )
        pv_if_called += face_value / (1 + treasury_rates[call_years] + spread / frequency) ** call_periods
        
        pv_if_not_called = sum(
            coupon_payment / (1 + treasury_rates[min(7, max(3, (i + 1) // frequency + 1))] + spread / frequency) ** (i + 1)
            for i in range(total_periods)
        )
        pv_if_not_called += face_value / (1 + treasury_rates[years] + spread / frequency) ** total_periods
        
        expected_value = call_probability * pv_if_called + (1 - call_probability) * pv_if_not_called
        return expected_value - bond_price
    
    oas_solution = opt.brentq(bond_price_with_spread, -0.1, 0.1)  # Solve for OAS
    return oas_solution * 10000  # Convert to basis points


def analyze_ytm_oas_relationship(face_value,
                                 coupon_rate,
                                 frequency,
                                 years,
                                 treasury_rates,
                                 call_years=3):
    """
    Analyzes the relationship between YTM and OAS for a callable bond.
    
    Args:
        coupon_rate (float): The bond's coupon rate.
        face_value (float): The bond's face value.
        treasury_rates (dict): Dictionary of Treasury rates by maturity.
        years (int): Years to maturity.
        call_years (int): Years until callable.
        
    Returns:
        tuple: (YTM values, OAS values, Price values)
    """
    # Generate YTM values ranging from Treasury rate to Treasury rate + 2%
    points = 40
    ytm_values = np.linspace(-0.01, 0.04, points, endpoint=True)\
                    + np.ones(points) * treasury_rates[call_years]
    
    # Calculate OAS for each YTM value
    oas_values = []
    
    for ytm in ytm_values:
        oas = calculate_oas_from_ytm(
            coupon_rate=coupon_rate,
            frequency=frequency,
            ytm=ytm,
            face_value=face_value,
            treasury_rates=treasury_rates,
            years=years,
            call_years=call_years
        )

        oas_values.append(oas)
    
    return ytm_values, oas_values