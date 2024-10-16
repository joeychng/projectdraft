from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)
api = os.getenv("API_TOKEN")

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/userprofile",methods=["GET","POST"])
def userprofile():
    return render_template('user_profile.html', api=api)
@app.put('/api/userprofile')
def update_userprofile():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    return jsonify({'message': 'Profile updated successfully!'}), 200

@app.route("/profile",methods=["GET","POST"])
def profile():
    return(render_template("profile.html"))

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