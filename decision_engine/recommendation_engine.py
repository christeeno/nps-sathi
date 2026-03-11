import math

def recommend_pension_scheme(user_profile: dict) -> dict:
    """
    Recommends between NPS and UPS based on age, service years, risk preference, and employment type.
    """
    age = user_profile.get("age", 30)
    years_of_service = user_profile.get("years_of_service", 0)
    risk_preference = user_profile.get("risk_preference", "moderate").lower()
    government_employee = user_profile.get("government_employee", False)

    # Simplified logic for demonstration:
    # UPS (Unified Pension Scheme) is highly beneficial for government employees 
    # with substantial service years looking for guaranteed returns.
    if government_employee and years_of_service >= 10 and risk_preference in ["low", "conservative"]:
        return {
            "recommended_scheme": "UPS",
            "reason": "As a government employee with 10+ years of service and low risk tolerance, the guaranteed pension of UPS offers better security."
        }
    
    # Otherwise, NPS is generally recommended for wealth accumulation, especially for younger/private sector.
    return {
        "recommended_scheme": "NPS",
        "reason": "NPS provides higher long-term market-linked returns, ideal for wealth accumulation given your profile and age."
    }

def recommend_monthly_contribution(current_forecast: dict, target_pension: float) -> float:
    """
    Calculates additional monthly contribution required if the projected pension falls short of the target.
    This uses a simplified linear approximation based on the existing forecast context.
    """
    projected_pension = current_forecast.get("monthly_pension", 0)
    current_contribution = current_forecast.get("monthly_contribution", 5000)
    
    if projected_pension >= target_pension or projected_pension == 0:
        return 0.0
    
    # Rough approximation: (Target / Projected) * Current Contribution - Current Contribution
    ratio = target_pension / projected_pension
    recommended_total = current_contribution * ratio
    additional_required = recommended_total - current_contribution
    
    return round(additional_required, 2)

def recommend_asset_allocation(age: int, risk_preference: str) -> dict:
    """
    Recommends an asset allocation strategy based on age and risk preference.
    """
    risk_preference = risk_preference.lower()
    
    # Base adjustments according to risk
    equity_adj = 0
    if risk_preference in ["high", "aggressive"]:
        equity_adj = 15
    elif risk_preference in ["low", "conservative"]:
        equity_adj = -15
        
    if age < 35:
        # Equity Heavy
        equity = min(75, 60 + equity_adj)
        bonds = (100 - equity) * 0.4
        govt = (100 - equity) * 0.6
    elif age <= 50:
        # Balanced
        equity = min(50, 40 + equity_adj)
        bonds = (100 - equity) * 0.5
        govt = (100 - equity) * 0.5
    else:
        # Conservative
        equity = max(10, 20 + equity_adj)
        bonds = (100 - equity) * 0.3
        govt = (100 - equity) * 0.7
        
    return {
        "equity": round(equity, 2),
        "bonds": round(bonds, 2),
        "government_securities": round(govt, 2)
    }

def generate_financial_advice(user_profile: dict) -> dict:
    """
    Combines forecast context, scheme recommendation, required contribution, and asset allocation
    into a unified actionable advice dictionary.
    """
    # 1. Scheme Recommendation
    scheme_rec = recommend_pension_scheme(user_profile)
    
    # 2. Asset Allocation
    age = user_profile.get("age", 30)
    risk_preference = user_profile.get("risk_preference", "moderate")
    allocation = recommend_asset_allocation(age, risk_preference)
    
    # 3. Contribution Recommendation (using placeholder target logic)
    # E.g., assume target pension is 50% of current monthly salary
    salary = user_profile.get("salary", 50000)
    target_pension = salary * 0.50
    
    current_contribution = user_profile.get("monthly_contribution", 5000)
    # Note: In a real system, we'd call the Phase 5/6 engines here to get the actual projected pension.
    # For this task's scope without circular importing/calling the full pipeline directly, we'll
    # simulate a quick proxy value based on the user_profile parameters to test the logic.
    proxy_projected_pension = current_contribution * 3.5  # Rough proxy for testing logic
    
    current_forecast = {
        "monthly_pension": proxy_projected_pension,
        "monthly_contribution": current_contribution
    }
    
    additional_contribution = recommend_monthly_contribution(current_forecast, target_pension)
    
    # 4. Retirement Score (Abstract 1-100 metric based on shortfall)
    score = 100
    if additional_contribution > 0:
        shortfall_ratio = additional_contribution / current_contribution
        score = max(10, int(100 - (shortfall_ratio * 50)))
        
    return {
        "retirement_score": score,
        "recommended_scheme": scheme_rec["recommended_scheme"],
        "scheme_reason": scheme_rec["reason"],
        "recommended_additional_contribution": additional_contribution,
        "target_pension_assumed": target_pension,
        "asset_allocation": allocation
    }
