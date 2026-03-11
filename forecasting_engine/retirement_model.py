def calculate_retirement_corpus(age: int, retirement_age: int, monthly_contribution: float, expected_return: float) -> float:
    """
    Calculates the projected retirement corpus based on monthly contributions.
    Uses the future value of a series formula: FV = P * (((1 + r)^n - 1) / r)
    """
    years_to_retirement = retirement_age - age
    if years_to_retirement <= 0:
        return 0.0

    months = years_to_retirement * 12
    # Convert annual expected return (e.g., 0.10) to a monthly rate
    monthly_rate = expected_return / 12

    if monthly_rate == 0:
        return float(monthly_contribution * months)

    corpus = monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    
    # We can also assume beginning of the month contribution: corpus *= (1 + monthly_rate)
    # The standard PMT FV formula. We'll use the end-of-month variant by default.
    return round(corpus, 2)

def estimate_pension_income(corpus: float, annuity_rate: float = 0.06) -> dict:
    """
    Estimates pension withdrawal based on NPS rules:
    - 60% can be withdrawn as a lump sum
    - 40% must be used to purchase an annuity
    """
    lump_sum_percent = 0.60
    annuity_percent = 0.40

    lump_sum = round(corpus * lump_sum_percent, 2)
    annuity_investment = round(corpus * annuity_percent, 2)

    annual_pension = annuity_investment * annuity_rate
    monthly_pension = round(annual_pension / 12, 2)

    return {
        "lump_sum": lump_sum,
        "annuity_investment": annuity_investment,
        "monthly_pension": monthly_pension
    }

def generate_retirement_forecast(user_profile: dict) -> dict:
    """
    Combines corpus calculation and pension estimation to provide a full forecast.
    
    user_profile expects at least:
    - age (int)
    - retirement_age (int)
    - monthly_contribution (float)
    - expected_return (float)
    """
    age = user_profile.get("age", 30)
    retirement_age = user_profile.get("retirement_age", 60)
    monthly_contribution = user_profile.get("monthly_contribution", 5000)
    expected_return = user_profile.get("expected_return", 0.10)

    projected_corpus = calculate_retirement_corpus(
        age=age,
        retirement_age=retirement_age,
        monthly_contribution=monthly_contribution,
        expected_return=expected_return
    )

    pension_details = estimate_pension_income(projected_corpus)

    return {
        "projected_corpus": projected_corpus,
        "lump_sum": pension_details["lump_sum"],
        "annuity_investment": pension_details["annuity_investment"],
        "monthly_pension": pension_details["monthly_pension"]
    }
