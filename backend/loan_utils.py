import pandas as pd

def calculate_emi(loan_amount, annual_rate, tenure_years):
    """
    Calculates EMI, interest, principal breakdown, and tax deduction.
    """
    monthly_rate = (annual_rate / 100) / 12
    tenure_months = tenure_years * 12

    # EMI formula: [P * r * (1 + r)^n] / [(1 + r)^n - 1]
    emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)

    # Amortization Schedule
    schedule = []
    remaining_balance = loan_amount
    total_interest = 0

    for i in range(1, tenure_months + 1):
        interest = remaining_balance * monthly_rate
        principal = emi - interest
        remaining_balance -= principal
        total_interest += interest
        schedule.append({"Month": i, "EMI": emi, "Principal": principal, "Interest": interest, "Balance": remaining_balance})

    df = pd.DataFrame(schedule)

    # Tax Benefits (Assumption: Max ₹2,00,000 deduction for home loans)
    tax_deduction = min(total_interest, 200000)

    return {
        "emi": round(emi, 2),
        "total_payment": round(emi * tenure_months, 2),
        "total_interest": round(total_interest, 2),
        "tax_deduction": round(tax_deduction, 2),
        "amortization": df.to_dict(orient="records")
    }
