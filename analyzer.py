def analyze_expenses(expenses, budgets):
    category_totals = {}
    for item in expenses:
        cat = item['category']
        category_totals[cat] = category_totals.get(cat, 0) + item['amount']

    violations = {}
    for category, total in category_totals.items():
        if total > budgets.get(category, float('inf')):
            violations[category] = {
                'spent': total,
                'budget': budgets[category]
            }
    return violations

def suggest_improvements(expenses):
    tips = []
    for item in expenses:
        if item["category"] == "Shopping" and item["amount"] > 1000:
            tips.append("Limit your shopping sprees 🛍️")
        if item["category"] == "Food" and item["amount"] > 500:
            tips.append("Try cooking at home more 🍳")
    return list(set(tips))  # remove duplicates
