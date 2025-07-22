from flask import Flask, render_template, request, redirect, url_for
from analyzer import analyze_expenses, suggest_improvements
from alerts import send_alert
from datetime import datetime

app = Flask(__name__)

# In-memory data (temporary)
expenses = []
budget = 80000  # Total budget
budgets = {
    "Food": 500,
    "Transport": 200,
    "Shopping": 1000,
    "Bills": 300,
    "Others": 200
}

# Budget alert logic
def check_budget(expenses_list):
    total = sum(e['amount'] for e in expenses_list)
    if total > budget:
        return "🚨 You've exceeded your budget!"
    elif total > 0.8 * budget:
        return "⚠️ You're nearing your budget limit."
    return None

# 🚀 Main route
@app.route('/', methods=['GET', 'POST'])
def index():
    category_filter = request.args.get('filter')
    filtered = expenses
    if category_filter:
        filtered = [e for e in expenses if e['category'] == category_filter]

    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])
        category = request.form['category']
        entry = {
            'description': description,
            'amount': amount,
            'category': category,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        expenses.append(entry)

        # Analyze this new entry
        violation = analyze_expenses([entry], budgets)
        if violation:
            send_alert(category, amount, budgets.get(category))

    # Calculate stats
    total = sum(e['amount'] for e in filtered)
    percent_used = min((total / budget) * 100, 100)
    alert_msg = check_budget(filtered)

    # Smart suggestions
    violations = analyze_expenses(filtered, budgets)
    suggestions = suggest_improvements(filtered)

    return render_template('index.html',
                           expenses=filtered,
                           alert=alert_msg,
                           total=total,
                           budget=budget,
                           percent_used=percent_used,
                           violations=violations,
                           suggestions=suggestions)

# ✅ Add route still works if you're using form action="/add"
@app.route('/add', methods=['POST'])
def add():
    category = request.form['category']
    amount = float(request.form['amount'])
    expenses.append({"category": category, "amount": amount})
    violation = analyze_expenses([{"category": category, "amount": amount}], budgets)
    if violation:
        send_alert(category, amount, budgets.get(category))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

