import numpy as np
from forecasting_engine.retirement_model import estimate_pension_income

def generate_market_return(mean_return: float, volatility: float) -> float:
    """
    Generates a random yearly return based on normal distribution.
    """
    return np.random.normal(mean_return, volatility)

def simulate_single_path(age: int, retirement_age: int, monthly_contribution: float, mean_return: float, volatility: float) -> float:
    """
    Simulates a single path of retirement corpus growth with random yearly returns.
    """
    years_to_retirement = retirement_age - age
    if years_to_retirement <= 0:
        return 0.0

    corpus = 0.0
    yearly_contribution = monthly_contribution * 12

    for _ in range(years_to_retirement):
        # Apply market return to existing corpus
        current_return = generate_market_return(mean_return, volatility)
        corpus *= (1 + current_return)
        
        # Add the yearly contribution (assuming it's added evenly over the year or end of year, 
        # standard is end of year for simple annual simulations)
        corpus += yearly_contribution
        
    return round(corpus, 2)

def run_monte_carlo_simulation(age: int, retirement_age: int, monthly_contribution: float, mean_return: float, volatility: float, simulations: int = 1000) -> dict:
    """
    Runs multiple simulations to find median, worst case, and best case scenarios.
    Returns the statistics and pension estimates for those cases.
    """
    all_simulations = []
    
    for _ in range(simulations):
        corpus = simulate_single_path(
            age=age,
            retirement_age=retirement_age,
            monthly_contribution=monthly_contribution,
            mean_return=mean_return,
            volatility=volatility
        )
        all_simulations.append(corpus)
        
    all_simulations = sorted(all_simulations)
    
    median_corpus = float(np.percentile(all_simulations, 50))
    worst_case_corpus = float(np.percentile(all_simulations, 10))
    best_case_corpus = float(np.percentile(all_simulations, 90))
    
    # Calculate pension estimates using the module from Phase 5
    median_pension = estimate_pension_income(median_corpus)
    worst_case_pension = estimate_pension_income(worst_case_corpus)
    best_case_pension = estimate_pension_income(best_case_corpus)
    
    return {
        "median_corpus": round(median_corpus, 2),
        "median_monthly_pension": median_pension["monthly_pension"],
        "worst_case_corpus": round(worst_case_corpus, 2),
        "worst_case_pension": worst_case_pension["monthly_pension"],
        "best_case_corpus": round(best_case_corpus, 2),
        "best_case_pension": best_case_pension["monthly_pension"],
        "all_simulations": all_simulations
    }
