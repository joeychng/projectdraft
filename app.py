from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key' 
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


user = {
    'name': 'Alice Lim',
    'email': 'Alicelim@gmail.com',
    'password': 'password123'
}

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_email = request.form.get('email')
        new_password = request.form.get('password')

        if new_name:
            user['name'] = new_name
        if new_email:
            user['email'] = new_email
        if new_password:
            user['password'] = new_password
        
        flash('Profile updated successfully!', 'success')

    return render_template('profile.html', user=user)


@app.route("/info", methods=["GET", "POST"])
def info():
    return render_template("info.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    balance = request.form.get("balance", 0)  # Default to 0 if not provided
    goal = request.form.get("goal", 0)  # Default to 0 if not provided
    try:
        balance = float(balance)
        goal = float(goal)
        if goal > 0:
            progress = (balance / goal) * 100
        else:
            progress = 0  # Avoid division by zero
    except ValueError:
        progress = 0  # Handle invalid input

    return render_template("dashboard.html", balance=round(balance, 2), progress=round(progress, 2))

@app.route("/goal", methods=["GET", "POST"])
def goal():
    return render_template("goal.html")

@app.route("/goal_results", methods=["GET", "POST"])
def goal_results():
    balance = request.form.get("balance", 0)
    retirementGoal = request.form.get("retirementGoal", 0)
    homePurchaseGoal = request.form.get("homePurchaseGoal", 0)
    targetYear1 = request.form.get("targetYear1")
    targetYear2 = request.form.get("targetYear2")

    try:
        balance = float(balance)
        retirementGoal = float(retirementGoal)
        status1 = (balance / retirementGoal) * 100 if retirementGoal > 0 else 0
    except ValueError:
        status1 = 0

    try:
        balance = float(balance)
        homePurchaseGoal = float(homePurchaseGoal)
        status2 = (balance / homePurchaseGoal) * 100 if homePurchaseGoal > 0 else 0
    except ValueError:
        status2 = 0

    return render_template("goal_results.html", retirementGoal=round(retirementGoal, 2), homePurchaseGoal=round(homePurchaseGoal, 2), targetYear1=targetYear1, targetYear2=targetYear2, status1=round(status1, 2), status2=round(status2, 2))

@app.route("/expense", methods=["GET", "POST"])
def expense():
    if request.method == 'POST':
        # Get data from the form
        category = request.form.get('category')  # Safely get the category field
        amount = request.form.get('amount')  # Safely get the amount field
        date = request.form.get('date')

        if not category or not amount or not date:
            return "Category, amount, or date missing!", 400

        try:
            amount = float(amount)
        except ValueError:
            return "Invalid amount!", 400

        # Initialize session if not already done
        if 'expenses' not in session:
            session['expenses'] = {}
        
        if date not in session['expenses']:
            session['expenses'][date] = {}

        # Update the expenses in session
        if category in session['expenses'][date]:
            session['expenses'][date][category] += amount
        else:
            session['expenses'][date][category] = amount

        return redirect(url_for('summary'))

    return render_template('expense.html')

@app.route("/summary", methods=["GET", "POST"])
def summary():
    expenses = session.get('expenses', {})
    
    # Initialize total expenses
    total_expenses = 0
    
    # Check if expenses is a dictionary
    if isinstance(expenses, dict):
        for date, categories in expenses.items():
            # Check if categories is a dictionary
            if isinstance(categories, dict):
                # Sum up only valid numeric amounts
                total_expenses += sum(amount for amount in categories.values() if isinstance(amount, (int, float)))
            else:
                print(f"Warning: Expected a dict for categories but got {type(categories)} for date {date}")

    return render_template('summary.html', expenses=expenses, total_expenses=total_expenses)


if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for development
