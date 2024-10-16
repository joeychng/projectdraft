from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

api_token = os.getenv("API_TOKEN")

# Define a User model to represent the users table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {"name": self.name, "email": self.email, "phone": self.phone}

# Create the database and the tables (only run this once)
@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/profile",methods=["GET","POST"])
def profile():
    user = User.query.get(1)
    return render_template('profile.html', user=user, api_token=api_token)
@app.route('/api/profile', methods=['PUT'])
def update_profile():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
   
    # Fetch user (you can fetch based on session or a dynamic user)
    user = User.query.get(1)  # Assuming we're updating the user with ID 1
    if not user:
        return jsonify({"error": "User not found"}), 404
    
     # Update the user's details
    user.name = name
    user.email = email
    user.phone = phone

    # Commit changes to the database
    db.session.commit()

    return jsonify({'message': 'Profile updated successfully!'}), 200

@app.route("/info",methods=["GET","POST"])
def info():
    return(render_template("info.html"))

@app.route("/dashboard",methods=["GET","POST"])
def dashboard():
    balance = request.form.get("balance")
    goal = request.form.get("goal")
    try:
        balance = float(balance)
        goal = float(goal)
        if goal > 0:
            progress = (balance / goal) * 100
        else:
            progress = 0  # Avoid division by zero if goal is zero
    except ValueError:
        # Handle case where input is not a valid number
        balance = 0
        goal = 0
        progress = 0
    return render_template("dashboard.html", balance=round(balance, 2), progress=round(progress, 2))

@app.route("/goal",methods=["GET","POST"])
def goal():
    return(render_template("goal.html"))

@app.route("/goal_results",methods=["GET","POST"])
def goal_results():
    balance = request.form.get("balance")
    retirementGoal = request.form.get("retirementGoal")
    homePurchaseGoal = request.form.get("homePurchaseGoal")
    targetYear1 = request.form.get("targetYear1")
    targetYear2 = request.form.get("targetYear2")
    try:
        balance = float(balance)
        retirementGoal = float(retirementGoal)
        if retirementGoal > 0:
            status1 = (balance / retirementGoal) * 100
        else:
            status1 = 0  # Avoid division by zero if goal is zero
    except ValueError:
        # Handle case where input is not a valid number
        balance = 0
        retirementGoal = 0
        status1 = 0

    try:
        balance = float(balance)
        homePurchaseGoal = float(homePurchaseGoal)
        if homePurchaseGoal > 0:
            status2 = (balance / homePurchaseGoal) * 100
        else:
            status2 = 0  # Avoid division by zero if goal is zero
    except ValueError:
        # Handle case where input is not a valid number
        balance = 0
        homePurchaseGoal = 0
        status2 = 0

    return(render_template("goal_results.html",retirementGoal=round(retirementGoal,2), homePurchaseGoal=round(homePurchaseGoal,2), targetYear1=targetYear1, targetYear2=targetYear2, status1=round(status1,2), status2=round(status2,2)))

if __name__ == "__main__":
    app.run()