def get_investment_recommendations(investments, medical_expenses, loan_interest, dependents):
    recommendations = []

    if investments < 150000:
        recommendations.append("Invest more in PPF, ELSS, or NPS to maximize 80C benefits.")
    
    if medical_expenses > 50000:
        recommendations.append("Check Section 80D deductions for additional medical expense benefits.")
    
    if loan_interest > 200000:
        recommendations.append("You may be eligible for additional home loan interest deductions under Section 24B.")

    if dependents > 2:
        recommendations.append("Consider tax-saving options like child education benefits under Section 80E.")

    if not recommendations:
        recommendations.append("Your tax planning looks optimized! Keep tracking your expenses and investments.")

    return recommendations
