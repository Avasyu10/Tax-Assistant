def generate_checklist(emp_type, has_investments, has_loans, has_business_income):
    checklist = ["✅ PAN Card", "✅ Aadhaar Card", "✅ Form 26AS (Tax Credit Statement)", "✅ Bank Statements"]

    if emp_type == "Salaried":
        checklist.append("✅ Form 16 (Salary Certificate from Employer)")
        checklist.append("✅ Payslips (Last 3 Months)")

    if emp_type == "Self-Employed" or has_business_income:
        checklist.append("✅ Income Proof (Bank Statements, Invoices, Balance Sheets)")
        checklist.append("✅ GST Returns (If applicable)")

    if has_investments:
        checklist.append("✅ Investment Proofs (PPF, NSC, ELSS, FD, etc.)")

    if has_loans:
        checklist.append("✅ Loan Interest Certificates (Home Loan, Education Loan)")

    checklist.append("✅ Receipts for Deductions (Medical Bills, Donations, etc.)")
    checklist.append("✅ Insurance Premium Receipts (Life & Health)")

    return checklist
