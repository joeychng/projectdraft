from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key' 
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Sample user data for demonstration (in real app, this would be stored in a database)
sample_user = {
    'name': 'Alice Lim',
    'email': 'alicelim@gmail.com',
    'password': '123456'
}
# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Fetch API token from environment
api_token = os.getenv("API_TOKEN")

# Define a User model to represent the users table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {"name": self.name, "email": self.email, "phone": self.phone}

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    user = User.query.get(1)  # Ensure this user exists

    if request.method == "POST":
        # Handle form submission to update user details
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        # Update the user's details
        if user:
            user.name = name
            user.email = email
            user.phone = phone
            try:
                db.session.commit()  # Commit changes to the database
            except Exception as e:
                print(f"Error saving profile: {e}")  # Print error for debugging

    return render_template('profile.html', user=user, api_token=api_token)

@app.route('/api/profile', methods=['PUT'])
def update_profile():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')

    user = User.query.get(1)  # Assuming we're updating the user with ID 1
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.name = name
    user.email = email
    user.phone = phone
    db.session.commit()

    return jsonify({'message': 'Profile updated successfully!'}), 200

@app.route('/profile2', methods=['GET', 'POST'])
def profile2():
    if request.method == 'POST':
        # Get updated data from form
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Store or update user data in session or database
        session['name'] = name
        session['email'] = email
        if password:
            session['password'] = password 

    return redirect(url_for('profile2'))
        
    user = {
        'name': session.get('name', ''),
        'email': session.get('email', ''),
    }

    # If GET request, render the profile page with current user data
    return render_template('profile2.html', user=user)


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

        if not category or not amount:
            return "Category or amount missing!", 400

        try:
            amount = float(amount)
        except ValueError:
            return "Invalid amount!", 400

        # Initialize session if not already done
        if 'expenses' not in session:
            session['expenses'] = {}

        # Update the expenses in session
        if category in session['expenses']:
            session['expenses'][category] += amount
        else:
            session['expenses'][category] = amount

        return redirect(url_for('summary'))

    return render_template('expense.html')

@app.route('/summary', methods=['GET'])
def summary():
    expenses = session.get('expenses', {})
    total_expenses = sum(expenses.values())
    return render_template('summary.html', expenses=expenses, total_expenses=total_expenses)

if __name__ == "__main__":
    with app.app_context():  # Ensure application context is active
        db.create_all()  # Ensure tables are created
    app.run(debug=True)  # Enable debug mode for development
