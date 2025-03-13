# Bond Analysis Project

## Overview

This project implements a comprehensive framework for analysing callable bonds using Monte Carlo simulations to estimate Option-Adjusted Spread (OAS). The analysis helps investors better understand the risk-return profile of callable bonds by modelling the probability of early redemption and its impact on yield.

## Project Structure

- **main.py**: The entry point of the application, orchestrating the data collection, analysis, and visualization
- **helpers/**
  - **dataCollection.py**: Fetches current treasury rates and market volatility
  - **finance.py**: Contains core financial calculation functions
  - **monteCarloSimulations.py**: Implements Monte Carlo methods for bond call probability and OAS calculation

## Key Financial Concepts

### Callable Bonds

A callable bond gives the issuer the right to redeem the bond before maturity at a predetermined price. This is typically done when interest rates decline, allowing the issuer to refinance at lower rates. For investors, this creates uncertainty about the investment horizon and potential returns.

### Option-Adjusted Spread (OAS)

OAS is a methodology that adjusts the spread over the benchmark (typically Treasury rates) to account for the embedded options in bonds. Unlike a simple yield spread, OAS considers:

- The probability of the bond being called
- The term structure of interest rates
- Interest rate volatility

A negative OAS indicates that the bond is trading at a premium relative to its option-adjusted value, suggesting the embedded call option is valuable to the issuer.

### Monte Carlo Simulation for Callable Bonds

The project uses Monte Carlo simulation to model potential interest rate paths and estimate:

1. The probability of a bond being called at the first call date
2. The fair value of the bond considering the call option
3. The appropriate OAS given market conditions

## Key Functions

### `dataCollection.py`

- `get_treasury_rates()`: Fetches current Treasury rates for different maturities using Yahoo Finance
- `get_implied_volatility()`: Estimates the volatility of Treasury yields using historical data

### `finance.py`

- `discount_cashflows()`: Computes the present value of future cash flows
- `calculate_bond_price()`: Determines the price of a bond given its YTM, coupon rate, and term

### `monteCarloSimulations.py`

- `determine_call_threshold()`: Calculates the interest rate level at which an issuer is likely to call the bond
- `mcs_call_probability()`: Uses Monte Carlo simulation to estimate the probability of the bond being called
- `calculate_oas_from_ytm()`: Computes the OAS for a given yield to maturity
- `analyze_ytm_oas_relationship()`: Explores how OAS changes across different YTM values

## Analysis Workflow

1. **Data Collection**:
   - Fetch current Treasury rates and implied market volatility

2. **Bond Parameter Definition**:
   - Set face value, coupon rate, frequency, maturity, and call protection period

3. **OAS Calculation**:
   - Calculate bond price based on YTM
   - Estimate call probability through Monte Carlo simulation
   - Compute OAS using numerical root-finding methods

4. **Visualization**:
   - Plot the relationship between YTM and OAS
   - Identify critical thresholds such as the Treasury rate at the call date and the zero-OAS point

## Mathematical Framework

The project implements several key mathematical concepts:

1. **Present Value Calculation**:

   $$
   PV = Σ (CF_t / (1 + r)^t)
   $$
   Where $CF_t$ is the cash flow at time $t$, and $r$ is the discount rate

2. **Call Probability Estimation**:
   Interest rates are modelled as a log-normal process with volatility derived from market data

3. **OAS Determination**:
   The OAS is the spread that equates the expected present value of the bond's cash flows (accounting for call probability) to its market price

## Usage Example

```python
# Define bond parameters
face_value = 1000
coupon_rate = 0.05
frequency = 2
years = 7
call_years = 3

# Get market data
treasury_rates = get_treasury_rates()
implied_volatility = get_implied_volatility()

# Calculate OAS
oas = calculate_oas_from_ytm(
    coupon_rate=coupon_rate,
    ytm=ytm,
    face_value=face_value,
    treasury_rates=treasury_rates,
    frequency=frequency,
    years=years,
    call_years=call_years
)
```

## Visualization

The project generates a plot showing the relationship between Yield to Maturity (YTM) and Option-Adjusted Spread (OAS). Key features of this visualization include:

- The point where OAS equals zero, indicating fair pricing
- The Treasury rate at the call date, a critical threshold for call likelihood
- The curve's shape, revealing how the option value changes with interest rates

## Dependencies

- `NumPy`: For numerical operations
- `Matplotlib`: For data visualization
- `SciPy`: For numerical optimization
- `yfinance`: For fetching financial data

## Notes for Future Enhancements

- Implement more sophisticated interest rate models (e.g., Hull-White, CIR)
- Add support for more complex bond structures (e.g., make-whole calls)
- Incorporate credit spread analysis for corporate bonds
- Expand visualization capabilities for sensitivity analysis
