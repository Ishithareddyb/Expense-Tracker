import os

def send_alert(category, spent, budget):
    print(f"🚨 ALERT: {category} limit exceeded! Spent ₹{spent} / ₹{budget}")
