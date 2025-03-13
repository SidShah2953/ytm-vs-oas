import yfinance as yf
import numpy as np


def get_treasury_rates():
    """
    Fetches the latest U.S. Treasury rates for different maturities.
    
    Returns:
        dict: A dictionary where keys are years (3, 4, 5, 6, 7) and valu    es are 
              the corresponding Treasury rates (as decimals).
    """
    tickers = {3: "^IRX", 4: "^FVX", 5: "^FVX", 6: "^TNX", 7: "^TNX"}
    treasury_rates = {}
    
    for year, ticker in tickers.items():
        try:
            data = yf.Ticker(ticker).history(period="1d")
            treasury_rates[year] = (
                data['Close'].iloc[-1] / 100 if not data.empty else 0.04
            )
        except Exception:
            # Default rates if fetching fails
            treasury_rates[year] = 0.04
    
    return treasury_rates


def get_implied_volatility():
    """
    Estimates the volatility of Treasury yields using historical data.
    
    Returns:
        float: Estimated annualized volatility of the Treasury rate.
    """
    try:
        ticker = "^TNX"  # 10-Year Treasury Yield
        data = yf.Ticker(ticker).history(period="1mo")
        
        if len(data) > 1:
            returns = np.diff(np.log(data['Close']))
            return np.std(returns) * np.sqrt(252)
    except Exception:
        pass
    
    return 0.012  # Default assumption (1.2% annualized volatility)