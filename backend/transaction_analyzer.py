import numpy as np
import pandas as pd

def analyze_transactions(df):

    df["Amount"] = df["Amount"].abs() 

    # Identify salary transactions
    salary_keywords = ["salary", "payroll", "wages", "income"]
    df["Category"] = np.where(df["Description"].str.contains("|".join(salary_keywords), case=False, na=False), 
                              "Salary", "Other")

    # Define expense categories
    expense_mapping = {
        "Rent": ["rent", "landlord"],
        "Groceries": ["grocery", "supermarket", "store", "food"],
        "Utilities": ["electricity", "water", "gas", "bill"],
        "Travel": ["uber", "taxi", "train", "bus", "flight"],
        "Entertainment": ["movie", "netflix", "concert", "show"],
        "Shopping": ["amazon", "flipkart", "shopping", "mall"],
        "Other Expenses": ["misc", "others"]
    }

    
    for category, keywords in expense_mapping.items():
        df.loc[df["Description"].str.contains("|".join(keywords), case=False, na=False), "Category"] = category


    df.loc[(df["Type"] == "Debit") & (df["Category"] == "Other"), "Category"] = "Other Expenses"


    df.loc[(df["Type"] == "Credit") & (df["Category"] == "Other"), "Category"] = "Other Income"

    monthly_summary = df.groupby(["Month", "Category"])["Amount"].sum().unstack(fill_value=0)

    
    monthly_summary["Total Income"] = monthly_summary.get("Salary", 0) + monthly_summary.get("Other Income", 0)
    monthly_summary["Total Expenses"] = monthly_summary.drop(columns=["Salary", "Other Income", "Total Income"], errors="ignore").sum(axis=1)
    monthly_summary["Net Savings"] = monthly_summary["Total Income"] - monthly_summary["Total Expenses"]

    # Add Overall Summary
    summary_row = monthly_summary.sum().to_frame().T
    summary_row.index = ["Overall Summary"]

    # Combine monthly breakdown and summary row
    result_table = pd.concat([monthly_summary, summary_row])

    return result_table.round(2)
