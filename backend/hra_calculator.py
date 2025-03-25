def calculate_hra(salary, hra_received, rent_paid, metro_city):
    """
    Calculate HRA exemption based on Indian tax rules.
    """
    basic_salary = 0.5 * salary  # Assuming Basic = 50% of Salary

    # Condition 1: Actual HRA received
    actual_hra = hra_received

    # Condition 2: Rent paid - 10% of Basic Salary
    rent_minus_10 = max(0, rent_paid - (0.1 * basic_salary))

    # Condition 3: 50% of Salary for Metro cities / 40% for Non-Metro
    metro_percentage = 0.5 if metro_city else 0.4
    metro_hra = metro_percentage * basic_salary

    # Find the minimum of the three conditions
    hra_exempted = min(actual_hra, rent_minus_10, metro_hra)

    # Taxable HRA = HRA received - Exempted HRA
    taxable_hra = max(0, actual_hra - hra_exempted)

    return {
        "actual_hra_received": actual_hra,
        "rent_minus_10_percent": rent_minus_10,
        "metro_or_non_metro_limit": metro_hra,
        "hra_exempted": hra_exempted,
        "hra_taxable": taxable_hra
    }
