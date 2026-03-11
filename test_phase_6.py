import json
import numpy as np

# Set random seed for deterministic testing
np.random.seed(42)

import sys
import os
# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from forecasting_engine.monte_carlo_simulator import run_monte_carlo_simulation

def run_phase_6_tests():
    print("--- Starting Phase 6: Monte Carlo Retirement Simulation Verification ---")
    
    age = 30
    retirement_age = 60
    monthly_contribution = 5000
    mean_return = 0.10
    volatility = 0.15
    simulations = 2000
    
    print(f"User Profile Input: Age {age}, Retires {retirement_age}, Contributes {monthly_contribution}/mo")
    print(f"Market Assumptions: Mean Return {mean_return*100}%, Volatility {volatility*100}%, SimRuns {simulations}")
    
    results = run_monte_carlo_simulation(
        age=age,
        retirement_age=retirement_age,
        monthly_contribution=monthly_contribution,
        mean_return=mean_return,
        volatility=volatility,
        simulations=simulations
    )
    
    # Exclude all_simulations array from JSON formatting for readability
    summary_results = {k: v for k, v in results.items() if k != "all_simulations"}
    
    print("\nSimulation Statistics Output:")
    print(json.dumps(summary_results, indent=4))
    
    # Assertions
    assert results["best_case_corpus"] > results["median_corpus"], "Best case should be greater than median"
    assert results["median_corpus"] > results["worst_case_corpus"], "Median should be greater than worst case"
    assert len(results["all_simulations"]) == simulations, "Simulation array length mismatch"
    
    print("\n✅ Verification successful. The Monte Carlo simulation structure is working correctly!")

if __name__ == "__main__":
    run_phase_6_tests()
