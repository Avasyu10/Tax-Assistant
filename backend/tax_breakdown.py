def calculate_tax_breakdown(income, investments, medical_expenses, loan_interest, dependents):
    # Calculate total deductions
    total_deductions = investments + medical_expenses + loan_interest + (dependents * 5000)
    taxable_income = max(0, income - total_deductions)

    # Estimate potential tax savings (assuming 20% savings)
    potential_savings = total_deductions * 0.2  

    # Breakdown dictionary
    breakdown = {
        "Income": income,
        "Deductions": total_deductions,
        "Taxable Income": taxable_income,
        "Potential Savings": potential_savings
    }

    return breakdown, potential_savings
