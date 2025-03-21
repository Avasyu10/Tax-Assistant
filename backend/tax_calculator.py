def calculate_tax(income):
    
    if income <= 1200000:
        tax = 0
    elif income <= 1600000:
        tax = (income - 1200000) * 0.15
    elif income <= 2000000:
        tax = (400000 * 0.15) + (income - 1600000) * 0.20
    elif income <= 2400000:
        tax = (400000 * 0.15) + (400000 * 0.20) + (income - 2000000) * 0.25
    else:
        tax = (400000 * 0.15) + (400000 * 0.20) + (400000 * 0.25) + (income - 2400000) * 0.30  # Assuming 30% for above 24L

    return tax
